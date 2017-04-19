


# from ..forms import Temp_ctxForm
# from .forms import CommentForm
# from .forms import ProjectForm

from ..models import Ctx


def get_app_ctx (app_name=None):
    return Ctx.objects.filter(app_name=app_name)
    
def post_app_ctx (ctx=None, app_name=None): 
    if len(get_app_ctx (app_name)) == 0 :
        obj = Ctx()
        obj.app_name = app_name
        obj.ctx = ctx
        obj.save()
    else :
        if get_app_ctx(app_name)[0].ctx != ctx :
            obj = Ctx()
            obj.app_name = "error_ctx"
            obj.ctx = "was " +str(get_app_ctx(app_name)[0].ctx) + " now : "+ str(ctx)
            obj.save()

            obj = get_app_ctx(app_name)[0]
            obj.ctx = ctx
            obj.save()

#one ctx by user by collab

# def get_current_collab ()