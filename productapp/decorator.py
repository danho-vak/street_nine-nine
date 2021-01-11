from django.http import HttpResponseRedirect

# User is admin?

def user_is_admin(func):
    def decorated(request, *args, **kwargs):
        if not request.user.is_admin:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # request 헤더에서 REFERER 주소로 되돌아 보냄
        return func(request, *args, **kwargs)
    return decorated