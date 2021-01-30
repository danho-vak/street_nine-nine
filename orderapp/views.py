from django.shortcuts import render
from django.views.generic import ListView

from orderapp.models import Order


class OrderListView(ListView):
    model = Order
    context_object_name = 'target_order'
    template_name = 'orderapp/list.html'

    def get_queryset(self):
        return Order.objects.get(user=self.request.user)
