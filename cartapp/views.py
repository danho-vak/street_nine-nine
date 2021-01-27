from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from productapp.models import Product

from cartapp.models import CartItem, Cart

#
#  CartItem을 생성하는 View
#    - ajax로 호출
#
#
def CartItemCreateView(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id', None)
        quantity = request.POST.get('quantity', 0)
        try:
            cart = Cart.objects.get(user=user)
            product = Product.objects.get(pk=product_id)
            product_option = product.product_option.first()

            # 새로운 CartItem object 생성
            new_item = CartItem(
                cart=cart,
                product=product,
                product_option=product_option,
                quantity=quantity
            )
            new_item.save()

            return redirect('productapp:detail', pk=product_id)

        except ObjectDoesNotExist:
            print('잘못된 카트 또는 상품 조회!')
            return False
    return False
