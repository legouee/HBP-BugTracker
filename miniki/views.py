
'''Views'''

from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import bleach

from markdown import markdown

from .forms import TicketPageForm
from .forms import HomeForm

from .models import TicketPage 
from .models import Home


from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse 

from hbp_app_python_auth.auth import get_access_token, get_token_type, get_auth_header
import hbp_app_python_auth.settings as auth_settings

import requests

from django.views.generic.list import ListView
from django.views.generic.base import  TemplateView, View
from django.views.generic.detail import DetailView

# def form_valid(self, form):

#     self.object = form.save()
#     print('blav')
#     # Envoi d'un message a l'utilisateur

#     messages.success(self.request, "Votre profil a ete mis a jour avec succes.")

#     return HttpResponseRedirect(self.get_success_url())

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )  #???
class HomeView(View):
    # context = UUID(request.GET.get('ctx'))
    template_name = "home.html"
    model = Home
    form_class = HomeForm
    

    def get(self, request, *args, **kwargs):
        import uuid
        context = uuid.uuid4()
        print ("request method",request.method)
        try:
            h = Home.objects.get(ctx=context)
            print('page exist')
        except Home.DoesNotExist:
            print('page does not exist')
            h = Home(ctx=context)

        form = self.form_class(instance = h)

        return render(request, self.template_name, {'form': form, 'ctx': str(context)})
    
    def post(self, request, *args, **kwargs):
        print("in post")
        form = self.form_class(request.POST)

        if form.is_valid():
            p = form.save(commit=False)
                 # Clean up user input
            p.save()
            return HttpResponseRedirect('home.html')
        return render(request, 'home.html', {'form': p, 'ctx': str(context)})

    # @classmethod
    # def create_Project(self, **kwargs):
    #     print("in create project")
        
    #     if request.method == 'POST':
    #         form = HomeForm(request.POST, instance=p)
    #     if form.is_valid():
    #         p = form.save(commit=False)
    #              # Clean up user input
    #         p.save()
    #     else:
    #         form = HomeForm(instance=p)

    #     return render(request,'home.html', {'new_project': new_project, 'content': content})
       
# @method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )  #???
# class CreateProjectView(ListView):
#     template_name = "home.html"
#     model = Home
#     import uuid
#     context = uuid.uuid4()
#     print (context)
#     try:
#         p = Home.objects.get(ctx=context)
#         content = markdown(p.text)
#     except Home.DoesNotExist:
#         p = None
#         content = ''

#     if request.method == 'POST':
#         form = HomeForm(request.POST, instance=p)
#     if form.is_valid():
#         p = form.save(commit=False)
#             # Clean up user input
#         p.save()
#     else:
#         form = HomeForm(instance=p)

#     #return render(request,'create_project.html', {'new_project': new_project, 'content': content})

@login_required(login_url='/login/hbp')
def show_ticket(request):
    '''Render the wiki page using the provided context query parameter'''
    print ("###############################################")
    print (request.GET.get('ctx'))
    print ("###############################################")
    
    # context = UUID(request.GET.get('ctx'))

    import uuid
    context = uuid.uuid4()
    print (context)

    try:
        ticket_page = TicketPage.objects.get(ctx=context)
        content = markdown(ticket_page.text)
    except TicketPage.DoesNotExist:
        ticket_page = None
        content = ''
    return render(request,'show_ticket.html', {'ticket_page': ticket_page, 'content': content})




@login_required(login_url='/login/hbp')
def edit_ticket(request):
    '''Render the wiki edit form using the provided cofrom django.conf import settings
from django.http import HttpResponseForbidden

from hbp_app_python_auth.auth import get_access_token, get_token_type, get_auth_header
import hbp_app_python_auth.settings as auth_settings
ntext query parameter'''

    if not _is_collaborator(request):
        return HttpResponseForbidden()

    context = UUID(request.GET.get('ctx'))
    # get or build the wiki page
    try:
        ticket_page = TicketPage.objects.get(ctx=context)
    except TicketPage.DoesNotExist:
        ticket_page = TicketPage(ctx=context)

    if request.method == 'POST':
        form = TicketPageForm(request.POST, instance=ticket_page)
        if form.is_valid():
            ticket_page = form.save(commit=False)
            # Clean up user input
            ticket_page.text = bleach.clean(ticket_page.text)
            ticket_page.save()
    else:
        form = TicketPageForm(instance=ticket_page)

    return render(request, 'edit.html', {'form': form, 'ctx': str(context)})

def _reverse_url(view_name, context_uuid):
    """generate an URL for a view including the ctx query param"""
    print ("Passing by view edit_ticket _reverse_url ?")
    
    return '%s?ctx=%s' % (reverse(view_name)  , context_uuid)

@login_required(login_url='/login/hbp')
def create_ticket(request):
    '''Render the wiki create form'''

    # if not _is_collaborator(request):
    #     return HttpResponseForbidden()

    # context = UUID(request.GET.get('ctx'))

    import uuid
    context = uuid.uuid4()
    print (context)

    # get or build the wiki page
    try:
        ticket_creation_page = TicketPage.objects.get(ctx=context)
        content = markdown(ticket_creation_page.text)
        print ("In create_ticket view : Try is ok")
    except TicketPage.DoesNotExist:
        ticket_creation_page = TicketPage(ctx=context)
        print ("In create_ticket view : Try not ok")
        
       

    if request.method == 'POST':
        print ("request.methodlogin_url == 'POST'")
        form = TicketPageForm(request.POST, instance=ticket_creation_page)

        if form.is_valid():
            print ("Yes form is valid")
            ticket_creation_page = form.save(commit=False)
            # Clean up user input
            ticket_creation_page.created_by = 1
            #ticket_creation_page.text = bleach.clean(ticket_creation_page.text)
            ticket_creation_page.save()
        else :
            print ("form not valid")
    else:
        print ("NOT request.method == 'post'")
        
        form = TicketPageForm(instance=ticket_creation_page)

    return render(request, 'create_ticket.html', {'form': form , 'ctx': str(context)})


def _is_collaborator(request):
    '''check access depending on context'''
    print ("Passing by view edit_ticket _is_collaborator ?")

    svc_url = settings.HBP_COLLAB_SERVICE_URL

    context = request.GET.get('ctx')
    if not context:
        return False
    url = '%scollab/context/%s/' % (svc_url, context)
    headers = {'Authorization': get_auth_header(request.user.social_auth.get())}

    #res = request.GET.get(url, headers=headers)
    
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        return False
    collab_id = res.json()['collab']['id']
    url = '%scollab/%s/permissions/' % (svc_url, collab_id)
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return False
    return res.json().get('UPDATE', False)



@login_required(login_url='/login/hbp')
def config(request):
    '''Render the config file'''

    res = requests.get(settings.HBP_ENV_URL)
    config = res.json()

    # Use this app client ID
    config['auth']['clientId'] = auth_settings.SOCIAL_AUTH_HBP_KEY

    # Add user token informations
    request.user.social_auth.get().extra_data
    config['auth']['token'] = {
        'access_token': get_access_token(request.user.social_auth.get()),
        'token_type': get_token_type(request.user.social_auth.get()),
        'expires_in': request.session.get_expiry_age(),
    }

    return JsonResponse(config)

class TicketListView(ListView):   #DetailView):   #ListView):
    
    model = TicketPage
    template_name = "ticket_list.html"
    #context = UUID(request.GET.get('ctx'))
    
    
    # def get_context_data(self, **kwargs):
    #     context = super(TicketListView, self).get_context_data(**kwargs)
    #     #context['now'] = timezone.now()
    #     return context



