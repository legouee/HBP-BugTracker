
'''Views'''

from django.shortcuts import render_to_response 
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_list_or_404
from django.shortcuts import get_object_or_404

from django.core.urlresolvers import reverse
from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import bleach

from markdown import markdown

#from .forms import TicketPageForm
from .forms import TicketForm
from .forms import HomeForm
from .forms import ProjectForm
#from .models import TicketPage
from .models import Ticket
from .models import Home
from .models import Project


from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseRedirect 

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

    import uuid
    context = uuid.uuid4()
    print (context)

    try:
        p = Project.objects.get(ctx=context)
        content = markdown(p.text) 
    except Project.DoesNotExist:                     
        p = Project(ctx=context)
        
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=p)

        if form.is_valid():
            p = form.save(commit=False)
            p.save()

    form = ProjectForm(instance=p)

    return render(request, 'create_project.html', {'form': form , 'ctx': str(context)})

@method_decorator(login_required(login_url='/login/hbp'), name='dispatch' )
class HomeView(TemplateView):
    # context = UUID(request.GET.get('ctx'))
    template_name = "home.html"
    model = Home
    form_class = HomeForm

    def projects(self):
        return Home.objects.get()

    def get(self, request, *args, **kwargs):
        import uuid
        context = uuid.uuid4()
        try:
            print("try")
            h = Home.objects.get()
            print (h)
        except Home.DoesNotExist:
            print("Home doesn't exist")
            h = Home(ctx=context)
        form = self.form_class(instance = h)

        return render(request, self.template_name, {'form': form, 'ctx': str(context)})
    
    def post(self, request, *args, **kwargs):
        import uuid
        context = uuid.uuid4()
        form = self.form_class(request.POST)
        if form.is_valid():
            print("is valid")
            form = form.save(commit=False)
                 # Clean up user input
            form.save()
        return render(request, self.template_name, {'form': form, 'ctx': str(context)})


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
        #ticket_page = TicketPage.objects.get(ctx=context)
        ticket = Ticket.objects.get(ctx=context)
        #content = markdown(ticket_page.text)
        content = markdown(ticket.text)
    #except TicketPage.DoesNotExist:  
    except Ticket.DoesNotExist:                  
        #ticket_page = None
        ticket = None
        content = ''
    #return render(request,'show_ticket.html', {'ticket_page': ticket_page, 'content': content})
    return render(request,'show_ticket.html', {'ticket': ticket, 'content': content})




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
        #ticket_page = TicketPage.objects.get(ctx=context)
        ticket = Ticket.objects.get(ctx=context)
    #except TicketPage.DoesNotExist:
    except Ticket.DoesNotExist:                    
        #ticket_page = TicketPage(ctx=context)
        ticket = Ticket(ctx=context)

    if request.method == 'POST':
        #form = TicketPageForm(request.POST, instance=ticket_page)
        #form = TicketForm(request.POST, instance=ticket_page)
        form = TicketForm(request.POST, instance=ticket)

        if form.is_valid():
            #ticket_page = form.save(commit=False)
            ticket = form.save(commit=False)
            # Clean up user input
            #ticket_page.text = bleach.clean(ticket_page.text)
            ticket.text = bleach.clean(ticket.text)
            #ticket_page.save()
            ticket.save()
    else:
        #form = TicketPageForm(instance=ticket_page)
        form = TicketForm(instance=ticket)

    return render(request, 'edit.html', {'form': form, 'ctx': str(context)})

def _reverse_url(view_name, context_uuid):
    """generate an URL for a view including the ctx query param"""
    print ("Passing by view edit_ticket _reverse_url ?")
    
    return '%s?ctx=%s' % (reverse(view_name)  , context_uuid)

@login_required(login_url='/login/hbp')
def create_ticket(request):
    '''Render the wiki create form'''

    import uuid
    context = uuid.uuid4()
    print (context)

    try:
        ticket_creation = Ticket.objects.get(ctx=context)
        content = markdown(ticket_creation.text) 
    except Ticket.DoesNotExist:                     
        ticket_creation = Ticket(ctx=context)
        
    if request.method == 'POST':

        form = TicketForm(request.POST, instance=ticket_creation)
        print (form)

        if form.is_valid():
            ticket_creation = form.save(commit=False)
            ticket_creation.created_by = 1
            ticket_creation.save()

        form = TicketForm(instance=ticket_creation)

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
    
    #model = TicketPage
    model = Ticket
    template_name = "ticket_list.html"
    #context = UUID(request.GET.get('ctx'))
    
    
    def get_context_data(self, **kwargs):
        context = super(TicketListView, self).get_context_data(**kwargs)
        #context['now'] = timezone.now()
        return context

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class TicketDetailView(DetailView):
    # model = TicketPage
    template_name = "ticket_detail.html"
    # slug_field = 'ticket_slug'

    # slug_url_kwarg = 'ticket_id' #need to acces to ticket id  #may be not usefull....

    context_object_name = 'context_object_name' #just in case

    #just for now
    queryset = Ticket.objects.all()


    def get_object(self):
        return get_object_or_404(Ticket, pk=1)

    # def get_object(self):
    #        object = get_object_or_404(TicketPage,title=self.kwargs['title'])
    #        return object

    def get_context_data(self, **kwargs):
        context = super(TicketDetailView, self).get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context

    def get_queryset(self):
        pass 
        #this should just return one to test