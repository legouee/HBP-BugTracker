


# from ..forms import Temp_ctxForm
# from .forms import CommentForm
# from .forms import ProjectForm

from ..models import Ctx


#we could welcome here all the function to handle future data of ctx tab

def get_collab_ctx (ctx=None):
    return Ctx.objects.filter(ctx=ctx)

def post_collab_ctx (ctx=None, collab=None):
    if len(get_app_ctx (ctx)) == 0 :
        obj = Ctx()
        obj.collab = collab
        obj.ctx = ctx
        obj.save()
    
    


# def get_app_ctx (ctx=None):
#     return Ctx.objects.filter(ctx=ctx)
    
# def post_app_ctx (ctx=None, app_name=None): 


#     if len(get_app_ctx (ctx)) == 0 :
#         obj = Ctx()
#         obj.app_name = app_name
#         obj.ctx = ctx
#         obj.save()

#     else :
#         if get_app_ctx(ctx)[0].ctx != ctx :
#             obj = Ctx()
#             obj.app_name = "error_ctx"
#             obj.ctx = "was " +str(get_app_ctx(app_name)[0].ctx) + " now : "+ str(ctx)
#             obj.save()

#             obj = get_app_ctx(app_name)[0]
#             obj.ctx = ctx
#             obj.save()
