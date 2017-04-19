


# from ..forms import Temp_ctxForm
# from .forms import CommentForm
# from .forms import ProjectForm

from ..models import Ctx

from django.conf import settings
from hbp_app_python_auth.auth import get_auth_header
import requests

#we could welcome here all the function to handle future data of ctx tab

def get_collab_ctx (ctx=None):
    return Ctx.objects.filter(ctx=ctx)

def post_collab_ctx (request=None, ctx=None ):
    if len(get_collab_ctx (ctx)) == 0 :
        obj = Ctx()
        obj.collab = get_collab_id (request=request, context=ctx)
        obj.ctx = ctx
        obj.save()
    
    
def get_collab_id (request=None, context=None):
    svc_url = settings.HBP_COLLAB_SERVICE_URL
    url = '%scollab/context/%s/' % (svc_url, context)
    headers = {'Authorization': get_auth_header(request.user.social_auth.get())}
    res = requests.get(url, headers=headers)
    collab_id = res.json()['collab']['id']

    return (collab_id)