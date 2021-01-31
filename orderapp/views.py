from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from cartapp.models import Cart
from orderapp.decorator import order_ownership
from orderapp.models import Order

USER_HAS_ORDER_OWNERSHIP = [order_ownership, login_required]


class OrderListView(ListView):
    model = Order
    context_object_name = 'target_order'
    template_name = 'orderapp/create.html'

    def get_queryset(self):
        #return Order.objects.get(user=self.request.user)
        return Cart.objects.get(user=self.request.user)


# @method_decorator(USER_HAS_ORDER_OWNERSHIP, 'dispatch')
class OrderCreateView(CreateView):
    model = Order
    fields = '__all__'
    success_url = ''
    template_name = 'orderapp/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['target_order'] = Cart.objects.get(user=self.request.user)

        return context

    def form_valid(self, form):
        pass