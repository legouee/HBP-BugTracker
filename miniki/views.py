
'''Views'''

from django.shortcuts import render_to_response, render, redirect
from django.core.urlresolvers import reverse
from uuid import UUID

from django.contrib.auth.decorators import login_required

import bleach

from markdown import markdown

from .forms import TicketPageForm, HomePageForm, TicketCreationPageForm
from .models import TicketPage, HomePage, TicketPageCreate


from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse 

from hbp_app_python_auth.auth import get_access_token, get_token_type, get_auth_header
import hbp_app_python_auth.settings as auth_settings

import requests

def form_valid(self, form):

    self.object = form.save()
    print('blav')
    # Envoi d'un message à l'utilisateur

    messages.success(self.request, "Votre profil a été mis à jour avec succès.")

    return HttpResponseRedirect(self.get_success_url())

@login_required(login_url='/login/hbp')
def home(request):
    #context = UUID(request.GET.get('ctx'))
    try:
        home_page = HomePage.objects.get()  #ctx=context)
        #content = markdown(home_page.text)
        content = 'Home page'
    except HomePage.DoesNotExist:
        home_page = None
        content = ''

    return render(request,'home.html', {'home_page': home_page, 'content': content})

@login_required(login_url='/login/hbp')
def show_ticket(request):
    '''Render the wiki page using the provided context query parameter'''
    #context = UUID(request.GET.get('ctx'))
    try:
        ticket_page = TicketPage.objects.get() #ctx=context)
        content = markdown(ticket_page.text)
    except TicketPage.DoesNotExist:
        ticket_page = None
        content = ''
    return render(request,'show_ticket.html', {'ticket_page': ticket_page, 'content': content})
    #render_to_response('show.html', {'wiki_page': wiki_page, 'content': content})



@login_required(login_url='/login/hbp')
def edit_ticket(request):
    '''Render the wiki edit form using the provided cofrom django.conf import settings
from django.http import HttpResponseForbidden

from hbp_app_python_auth.auth import get_access_token, get_token_type, get_auth_header
import hbp_app_python_auth.settings as auth_settings
ntext query parameter'''

    if not _is_collaborator(request):
        return HttpResponseForbidden()

    #context = UUID(request.GET.get('ctx'))
    # get or build the wiki page
    try:
        ticket_page = TicketPage.objects.get() #ctx=context)
    except TicketPage.DoesNotExist:
        ticket_page = TicketPage() #ctx=context)

    if request.method == 'POST':
        form = TicketPageForm(request.POST, instance=ticket_page)
        if form.is_valid():
            ticket_page = form.save(commit=False)
            # Clean up user input
            ticket_page.text = bleach.clean(ticket_page.text)
            ticket_page.save()
    else:
        form = TicketPageForm(instance=ticket_page)

    return render(request, 'edit.html', {'form': form,  })#'ctx': str(context)})

def _reverse_url(view_name, context_uuid):
    """generate an URL for a view including the ctx query param"""
    print ("Passing by view edit_ticket _reverse_url ?")
    
    return '%s?ctx=%s' % (reverse(view_name)  , context_uuid)

@login_required(login_url='/login/hbp')
def create_ticket(request):
    '''Render the wiki create form'''

    if not _is_collaborator(request):
        return HttpResponseForbidden()

    #context = UUID(request.GET.get('ctx'))
    # get or build the wiki page
    try:
        ticket_creation_page = TicketPageCreate.objects.get() #ctx=context)
        content = markdown(ticket_creation_page.text)
    except TicketPageCreate.DoesNotExist:
        ticket_creation_page = TicketPageCreate() #ctx=context)
       

    if request.method == 'post':
        form = TicketCreationPageForm(request.POST, instance=ticket_creation_page)
        if form.is_valid():
            ticket_creation_page = form.save(commit=False)
            # Clean up user input
            ticket_creation_page.created_by = 1
            #ticket_creation_page.text = bleach.clean(ticket_creation_page.text)
            ticket_creation_page.save()
    else:
        form = TicketCreationPageForm(instance=ticket_creation_page)

    return render(request, 'create_ticket.html', {'form': form  })#'ctx': str(context)})

def _reverse_url(view_name, context_uuid):
    """generate an URL for a view including the ctx query param"""
    print ("Passing by view create_ticket _reverse_url ?")
    
    return '%s?ctx=%s' % (reverse(view_name)  , context_uuid)

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