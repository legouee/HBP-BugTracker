
'''Views'''

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect 

from hbp_app_python_auth.auth import get_access_token, get_token_type, get_auth_header
import hbp_app_python_auth.settings as auth_settings
import requests

from django.views.generic.list import ListView
from django.views.generic.base import  TemplateView, View
from django.views.generic.detail import DetailView

from django.shortcuts import render_to_response 
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404

from django.core.urlresolvers import reverse
from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import bleach

from markdown import markdown
from .forms import TicketForm

from .forms import CommentForm
from .forms import ProjectForm

from .models import Ticket

from .models import Project
from .models import Comment
from .models import Ctx

from .utils.ctx_handler import post_collab_ctx, get_collab_ctx, remove_ticket, close_ticket,open_ticket, get_collab_name, handle_ctxstate
import json
from django.core import serializers

from django.views.decorators.csrf import csrf_protect, csrf_exempt

from django.http import HttpResponse

from django.template import RequestContext

from django.core import serializers

class ProjectListView(ListView): 
    model = Project
    template_name = "project_list.html"

    def get_context_data(self, **kwargs):
        context = super(ProjectListView, self).get_context_data(**kwargs)
        return context

    def projects(self):
        return Project.objects.filter()

@login_required(login_url='/login/hbp')
def create_project(request):
    '''Render the wiki create form'''

    try:
        p = Project.objects.get()
        content = markdown(p.text) 
    except Project.DoesNotExist:                
        p = Project()
        
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=p)

        if form.is_valid():
            p = form.save(commit=False)
            p.save()

    form = ProjectForm(instance=p)

    return render(request, 'create_project.html', {'form': form, 'ctx': self.kwargs['ctx']})


@login_required(login_url='/login/hbp')
def Test_Menu_deroulant(request):
    '''Render the wiki page using the provided context query parameter''' 
    try:
        ticket = Ticket.objects.get(ctx=context)
        content = markdown(ticket.text)  
    except Ticket.DoesNotExist:                  
        ticket = None
        content = ''
    return render(request,'Test_Menu_deroulant.html', {'ticket': ticket, 'content': content})

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class CreateTicketView(TemplateView):

    template_name = "create_ticket.html"
    model = Ticket
    form_class = TicketForm

    def get(self, request, *args, **kwargs):

        if not _is_collaborator(request, self.kwargs['ctx']):
            return HttpResponseForbidden()

        h = Ticket()
        form = self.form_class(instance = h)

        return render(request, self.template_name, {'form': form, 'ctx': self.kwargs['ctx'], 'collab_name':get_collab_name(self.kwargs['ctx'])})
    
    def post(self, request, *args, **kwargs):
        ticket_creation = Ticket()
        ticket_creation.ctx = get_object_or_404(Ctx, ctx=self.kwargs['ctx'])
        form = self.form_class(request.POST, instance=ticket_creation)

        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.save()
            return self.redirect(request, ctx = self.kwargs['ctx'])
        return render(request, self.template_name, {'form': form, 'ctx': self.kwargs['ctx'], 'collab_name':get_collab_name(self.kwargs['ctx'])})

    @classmethod    
    def redirect(self, request, *args, **kwargs): ### use to go back to TicketListView directly after creating a ticket
        url = reverse('ticket-list2', kwargs = {'ctx': kwargs['ctx']})

        return HttpResponseRedirect(url)

def _is_collaborator(request, context):
    '''check access depending on context'''
    svc_url = settings.HBP_COLLAB_SERVICE_URL
    if not context:
        return False

    url = '%scollab/context/%s/' % (svc_url, context)

    headers = {'Authorization': get_auth_header(request.user.social_auth.get())}
    print("request:", request)
    res = requests.get(url, headers=headers)
    print("here ",res)
    if res.status_code != 200:
        return False

    collab_id = res.json()['collab']['id']
    url = '%scollab/%s/permissions/' % (svc_url, collab_id)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return False
    return res.json().get('UPDATE', False)

def _get_collab_extension(request, context):
    svc_url = settings.HBP_COLLAB_SERVICE_URL
    url = '%scollab/context/%s/' % (svc_url, context)

    headers = {'Authorization': get_auth_header(request.user.social_auth.get())}

    res = requests.get(url, headers=headers)
    # print ("RES 1 ")
    # print(res.__dict__)
    # for key, value in res.__dict__.items():
    #     print (key)
    #     print (value)

    print (json.loads(res._content)['collab']['title'])
    return (json.loads(res._content)['collab']['title'])



def _get_access_token(request):
    return request.user.social_auth.get().extra_data['access_token']

@login_required(login_url='/login/hbp')
def config(request):
    '''Render the config file'''
    res = requests.get(settings.HBP_ENV_URL)
    config = res.json()

    # Use this app client ID
    config['auth']['clientId'] = auth_settings.SOCIAL_AUTH_HBP_KEY

    # Add user token informations
    config['auth']['token'] = {
        'access_token': _get_access_token(request),
        'token_type': get_token_type(request.user.social_auth.get()),
        'expires_in': request.session.get_expiry_age(),
    }
    
    # test = requests.get
    return JsonResponse(config)

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class TicketListView(ListView):  

    model = Ticket
    template_name = "ticket_list.html"


    def get(self, request, *args, **kwargs):

        # for key, value in request.__dict__.items(): 
        #     try :
        #         for key2, value2 in value.items() :
        #             try :
        #                 for key3, value3 in value2.items() :
        #                     print (key3, value3)        
        #             except :
        #                 print (key2, value2)       
        #     except :
        #         print (key, value)

        ctx, pk = handle_ctxstate(request)  
        
        if not _is_collaborator(request, ctx):
            return HttpResponseForbidden()

        if pk : #if pk found in ctxstate then we need to redirect the user
            return self.redirect(request, pk=pk, ctx=ctx)
             

        project_name = _get_collab_extension(request, ctx) #need to change the name
        post_collab_ctx (request=request,ctx=ctx, project_name=project_name )

        current_base_ctx = Ctx.objects.filter(ctx=ctx)
        tickets = Ticket.objects.filter(ctx_id=current_base_ctx[0].id) 
        ## add number of comments
        for ticket in tickets:
            ticket.nb_coms = self.get_nb_com(ticket.pk)                     
            
        return render(request, self.template_name, {'object': tickets, 'ctx': ctx, 'collab_name':get_collab_name(ctx)}) #will nedd to replace all() by filter project
    
    @classmethod  
    def get_nb_com(self, pk):
        return Comment.objects.filter(ticket_id= pk).count()

    @classmethod    
    def redirect(self, request, *args, **kwargs): 
        url = reverse('ticket-detail', kwargs = { 'pk':kwargs['pk'],'ctx': kwargs['ctx']})
        return HttpResponseRedirect(url)

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class TicketListView2(ListView):  
    model = Ticket
    template_name = "ticket_list.html"

    def get(self, request, *args, **kwargs):
        if not _is_collaborator(request, self.kwargs['ctx']):
            return HttpResponseForbidden()

        current_base_ctx = Ctx.objects.filter(ctx=self.kwargs['ctx']) 
        tickets = Ticket.objects.filter(ctx_id=current_base_ctx[0].id)

        ## add number of comments
        for ticket in tickets:
            ticket.nb_coms = self.get_nb_com(ticket.pk) 
        
        return render(request, self.template_name, {'object': tickets, 'ctx': self.kwargs['ctx'], 'collab_name':get_collab_name(self.kwargs['ctx'])}) #will nedd to replace all() by filter project


    @classmethod  
    def get_nb_com(self, pk):
        return Comment.objects.filter(ticket_id= pk).count()

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class TicketDetailView(DetailView):

    model = Comment
    template_name = "ticket_detail.html"
    form_class = CommentForm

    def get_object(self,request):
        comments= Comment.objects.filter(ticket_id = self.kwargs['pk'])
        for comment in comments:
            comment.is_author = self.check_user_is_author(request,comment)
        ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
        ticket.is_author = self.check_user_is_author(request,ticket)
        
        return [comments, ticket ]
        
    def get_queryset (self):        
        return get_object_or_404(Ticket, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):   
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):


        # for key, value in request.__dict__.items(): 
        #     try :
        #         for key2, value2 in value.items() :
        #             try :
        #                 for key3, value3 in value2.items() :
        #                     print (key3, value3)        
        #             except :
        #                 print (key2, value2)       
        #     except :
        #         print (key, value)

        if not _is_collaborator(request, self.kwargs['ctx']):
            return HttpResponseForbidden()
            
        cmt = Comment()
        form = self.form_class(instance = cmt)

        return render(request, self.template_name, {'form': form, 'object': self.get_object(request), 'ctx': self.kwargs['ctx'], 'collab_name':get_collab_name(self.kwargs['ctx']) })    

    @classmethod    
    def redirect(self, request, *args, **kwargs): 
        url = reverse('ticket-detail', kwargs = { 'pk':kwargs['pk'],'ctx': kwargs['ctx']})
        return HttpResponseRedirect(url)
    
    #@csrf_exempt
    def post(self, request, *args, **kwargs):
       
        if request.POST.get('action', None) == 'edit_ticket':
           form=self.edit_ticket(request)
        else:
            if request.POST.get('action', None) == 'edit_comment':
                form=self.edit_comment(request)
            else:
             
                comment_creation = Comment()
                comment_creation.ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])      
       
                if request.method == 'POST':
                    form = CommentForm(request.POST, instance=comment_creation)

                    if form.is_valid():
                        form = form.save(commit=False)
                        form.author = request.user
                        form.save()
                        return self.redirect(request, pk=self.kwargs['pk'], ctx=self.kwargs['ctx'])
                    else :
                        form = CommentForm(instance=comment_creation)
                #faire passer un message...
   
        return render(request, 'ticket_detail.html', {'form': form, 'ctx': self.kwargs['ctx'],'collab_name':get_collab_name(self.kwargs['ctx'])})          

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL
        """
        model_instance = form.save(commit=False)
        model_instance.ticket = self.object
        model_instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def edit_ticket(self,request):
        ticket_id = request.POST.get('pk')
        queryset = Ticket.objects.get(pk = ticket_id)

        form = TicketForm(request.POST, instance=queryset)
        form.title = request.POST.get('title')
        form.text = request.POST.get('text')

        if form.is_valid():
            form.save()

        return form

    def edit_comment(self,request):
        comment_id = request.POST.get('pk')
        queryset = Comment.objects.get(pk = comment_id)

        form = CommentForm(request.POST, instance=queryset)
        form.text = request.POST.get('text')

        if form.is_valid():
            form.save()

        return form

    def check_user_is_author(self,request,_object):
            if str(request.user) == str(_object.author):
                return True
            else: return False 


@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class AdminTicketListView(ListView):  
    model = Ticket
    template_name = "admin_ticket_list.html"

    def get(self, request, *args, **kwargs):

        ctx, pk = handle_ctxstate (request)

        if not _is_collaborator(request, ctx):
            return HttpResponseForbidden()
        
        if pk : #if pk found in ctxstate then we need to redirect the user
            return self.redirect(request, pk=pk, ctx=ctx)


        project_name = _get_collab_extension(request, ctx) #need to change the name
        post_collab_ctx (request=request,ctx=ctx, project_name=project_name )

        current_base_ctx = Ctx.objects.filter(ctx=ctx) 
        tickets = Ticket.objects.filter(ctx_id=current_base_ctx[0].id)

        ## add number of comments
        for ticket in tickets:
            ticket.nb_coms = self.get_nb_com(ticket.pk) 
        
        # tickets= serializers.serialize("json", tickets)
        # # print (tickets)

        return render(request, self.template_name, {'object': tickets, 'ctx': ctx, 'collab_name':get_collab_name(ctx)})

    @classmethod  
    def get_nb_com(self, pk):
        return Comment.objects.filter(ticket_id= pk).count()

    @classmethod    
    def redirect(self, request, *args, **kwargs): 
        url = reverse('ticket-detail-admin', kwargs = { 'pk':kwargs['pk'],'ctx': kwargs['ctx']})
        return HttpResponseRedirect(url)


@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class AdminTicketListView2(ListView):  
    model = Ticket
    template_name = "admin_ticket_list.html"

    def get(self, request, *args, **kwargs):
        print ("I pass by GET in AdminTicketListView2")
        
        print (self.kwargs)
        print ("ctx : V2 : " +str(self.kwargs['ctx']) )

        if not _is_collaborator(request, self.kwargs['ctx']):
            return HttpResponseForbidden()

        current_base_ctx = Ctx.objects.filter(ctx=self.kwargs['ctx']) 
        tickets = Ticket.objects.filter(ctx_id=current_base_ctx[0].id)

        ## add number of comments
        for ticket in tickets:
            ticket.nb_coms = self.get_nb_com(ticket.pk) 
        

        return render(request, self.template_name, {'object': tickets, 'ctx': self.kwargs['ctx'], 'collab_name':get_collab_name(self.kwargs['ctx'])})
        # return render_to_response (self.template_name, {'object': tickets, 'ctx': self.kwargs['ctx']}, context_instance=RequestContext(request))

    @classmethod  
    def get_nb_com(self, pk):
        return Comment.objects.filter(ticket_id= pk).count()

    @classmethod    
    def redirect(self, request, *args, **kwargs): 
        url = reverse('ticket-admin2', kwargs = { 'ctx': kwargs['ctx']})
        print ("dddddd")
        return HttpResponseRedirect(url)

    # @csrf_exempt
    def post(self, request, *args, **kwargs):

        if json.loads(request.POST.get('action', None)) == 'close':
            close_ticket (request)

        elif json.loads(request.POST.get('action', None)) == 'open':
            open_ticket (request)
      
        print ("I pass by POST in AdminTicketListView2")
        return self.redirect(request, ctx=self.kwargs['ctx'])
        # return render_to_response( self.template_name, { 'ctx': self.kwargs['ctx']} )
        # return render(request, self.template_name, {'ctx': self.kwargs['ctx']})
        

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class AdminTicketDetailView(DetailView):

    model = Comment
    template_name = "admin_ticket_detail.html"
    form_class = CommentForm

    # def get_object(self):
    #     return [Comment.objects.filter(ticket_id = self.kwargs['pk']), get_object_or_404(Ticket, pk=self.kwargs['pk']) ]

    def get_object(self,request):
        comments=Comment.objects.filter(ticket_id = self.kwargs['pk'])
        for comment in comments:
            comment.is_author = self.check_user_is_author(request,comment)
            print(comment.is_author)
        ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])
        ticket.is_author = self.check_user_is_author(request,ticket)
        
        return [comments, ticket ]
        
    def get_queryset (self):        
        return get_object_or_404(Ticket, pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):   
        context = super(AdminTicketDetailView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):

        if not _is_collaborator(request, self.kwargs['ctx']):
            return HttpResponseForbidden()
            
        cmt = Comment()
        form = self.form_class(instance = cmt)

        return render(request, self.template_name, {'form': form, 'object': self.get_object(request), 'ctx': self.kwargs['ctx'], 'collab_name':get_collab_name(self.kwargs['ctx']) })    

    @classmethod    
    def redirect(self, request, *args, **kwargs): ### use to go back to TicketListView directly after creating a ticket
        url = reverse('ticket-detail-admin', kwargs = { 'pk':kwargs['pk'],'ctx': kwargs['ctx']})
        return HttpResponseRedirect(url)

    def post(self, request, *args, **kwargs):
       
        if request.POST.get('action', None) == 'edit_ticket':
           form=self.edit_ticket(request)
        else:
            comment_creation = Comment()
            comment_creation.ticket = get_object_or_404(Ticket, pk=self.kwargs['pk'])      
       
            if request.method == 'POST':
                form = CommentForm(request.POST, instance=comment_creation)

                if form.is_valid():
                    form = form.save(commit=False)
                    form.author = request.user
                    form.save()
                    return self.redirect(request, pk=self.kwargs['pk'], ctx=self.kwargs['ctx'])
                else :
                    form = CommentForm(instance=comment_creation)
                #faire passer un message...
   
        return render(request, 'ticket_detail.html', {'form': form, 'ctx': self.kwargs['ctx'],'collab_name':get_collab_name(self.kwargs['ctx'])}) 



    def edit_ticket(self,request):
        ticket_id = request.POST.get('pk')
        queryset = Ticket.objects.get(pk = ticket_id)

        form = TicketForm(request.POST, instance=queryset)
        form.title = request.POST.get('title')
        form.text = request.POST.get('text')

        if form.is_valid():
            form.save()

        return form





    def check_user_is_author(self,request,_object):
            if str(request.user) == str(_object.author):
                return True
            else: return False 