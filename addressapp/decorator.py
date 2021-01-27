from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from addressapp.models import UserAddress


def address_ownership(func):
    def decorated(request, *args, **kwargs):
        try:
            address = UserAddress.objects.get(pk=kwargs['pk'])
        except ObjectDoesNotExist:
            address = None

        if not address.target_user == request.user:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # request 헤더에서 REFERER 주소로 되돌아 보냄

        return func(request, *args, **kwargs)
    return decorated