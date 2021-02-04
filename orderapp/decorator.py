from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from orderapp.models import Order


def order_ownership(func):
    def decorated(request, *args, **kwargs):
        try:
            order = Order.objects.filter(user=request.user)
        except ObjectDoesNotExist:
            order = None

        if not order.user == request.user:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # request 헤더에서 REFERER 주소로 되돌아 보냄

        return func(request, *args, **kwargs)
    return decorated