


# from ..forms import Temp_ctxForm
# from .forms import CommentForm
# from .forms import ProjectForm

from ..models import Ctx
from ..models import Ticket
from ..models import Project
from ..models import Comment



from django.conf import settings
from hbp_app_python_auth.auth import get_auth_header
import requests

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse


from django.shortcuts import get_object_or_404

import json
# from django.views.decorators.csrf import csrf_protect, csrf_exempt


# from flask import Flask, request

#we could welcome here all the function to handle future data of ctx tab

def get_collab_name (ctx=None):
    return get_object_or_404(Ctx, ctx=ctx).project_name

def get_collab_ctx (ctx=None):
    return Ctx.objects.filter(ctx=ctx)

def post_collab_ctx (request=None, ctx=None, project_name=None ):
    if len(get_collab_ctx (ctx)) == 0 :
        obj = Ctx()
        obj.collab = _get_hbp_collab_id (request=request, context=ctx)
        obj.ctx = ctx
        obj.project_name = project_name
        obj.save()
    
    
def _get_hbp_collab_id (request=None, context=None):
    svc_url = settings.HBP_COLLAB_SERVICE_URL
    url = '%scollab/context/%s/' % (svc_url, context)
    headers = {'Authorization': get_auth_header(request.user.social_auth.get())}
    res = requests.get(url, headers=headers)
    collab_id = res.json()['collab']['id']

    return (collab_id)



# @csrf_exempt
def remove_ticket (request):
    ticket_id = request.POST.get('pk', None)
    ticket_id = json.loads(ticket_id)
    for pk in ticket_id :
        Ticket.objects.filter(id=pk).delete()

   

def close_ticket (request):
    ticket_id = request.POST.get('pk', None)
    ticket_id = json.loads(ticket_id)
    for pk in ticket_id :
        # ticket = Ticket.objects.filter(id=pk)
        ticket = get_object_or_404(Ticket, pk=pk)

        ticket.status = 'closed'
        ticket.save()

  

def open_ticket (request):
    ticket_id = request.POST.get('pk', None)
    ticket_id = json.loads(ticket_id)
    for pk in ticket_id :
        # ticket = Ticket.objects.filter(id=pk)
        ticket = get_object_or_404(Ticket, pk=pk)

        ticket.status = 'open'
        ticket.save()

    

def get_ctx_ctxstate (request):
    try :
        ctx, ctxstate = request.META['QUERY_STRING'][4:].split("&")
    except:
        print ("Except")
        ctx = request.META['QUERY_STRING'][4:]
        ctxstate = None
    return (ctx, ctxstate)

def handle_ctxstate (request):
    ctx, ctxstate = get_ctx_ctxstate (request)

    if ctxstate != None :
        pk  = ctxstate[-1]
      
        if pk == 'n': #this is the list
            return (ctx, None)
        else : #this is a ticket detail
            return (ctx, pk)
    
    print (ctx)
    print (ctxstate)
    

    return (ctx, None)
