


# from ..forms import Temp_ctxForm
# from .forms import CommentForm
# from .forms import ProjectForm

from ..models import Ctx


def get_temp_user_ctx (user_name=None):
    return Ctx.objects.filter(user_name=user_name)
    
def post_temp_user_ctx (ctx=None, user_name=None): 
    if len(get_temp_user_ctx (user_name)) == 0 :
        obj = Ctx()
        obj.user_name = user_name
        obj.ctx = ctx
        obj.save()
    else :
        if get_temp_user_ctx(user_name)[0].ctx != ctx :
            obj = Ctx()
            obj.user_name = "error_ctx"
            obj.ctx = "was " +str(get_temp_user_ctx(user_name)[0].ctx) + " now : "+ str(ctx)
            obj.save()

            obj = get_temp_user_ctx(user_name)[0]
            obj.ctx = ctx
            obj.save()

#one ctx by user by collab

# def get_current_collab ()