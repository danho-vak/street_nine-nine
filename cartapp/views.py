from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView

from cartapp.models import Cart
from productapp.models import Product


def AddCartView(request):
    if request.method == 'post':
        user = request.user
        product_id = request.POST.get('product_pk')

        product = Product.objects.get(pk=product_id)

        try:
            cart = Cart.objects.get(user=user)
            new_item = cart()
            new_item.user = user
            new_item.product = product
            new_item.quantity += 1
            new_item.save()

        except:
            print('카트 없음!')
