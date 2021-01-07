from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from accountapp.models import User


def account_has_ownership(func):
    def decorated(request, *args, **kwargs):
        try:
            user = User.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            user = None

        if not user == request.user:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # request 헤더에서 REFERER 주소로 되돌아 보냄

        return func(request, *args, **kwargs)
    return decorated
