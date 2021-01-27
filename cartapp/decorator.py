from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect

from addressapp.models import UserAddress
from cartapp.models import Cart, CartItem


def cart_ownership(func):
    def decorated(request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
        except ObjectDoesNotExist:
            cart = None

        if not cart.user == request.user:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # request 헤더에서 REFERER 주소로 되돌아 보냄

        return func(request, *args, **kwargs)
    return decorated