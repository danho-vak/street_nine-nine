from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView

from cartapp.decorator import cart_ownership
from productapp.models import Product

from cartapp.models import CartItem, Cart


USER_HAS_CART_OWNERSHIP = [cart_ownership, login_required]

#
#  해당 User의 Cart를 가져오는 View
#    - request.user로 해당 user의 Cart를 가져오고 template에서 참조된 CartItem을 처리
#
method_decorator(USER_HAS_CART_OWNERSHIP, 'get')
class CartListView(ListView):
    model = Cart
    context_object_name = 'target_cart'
    template_name = 'cartapp/list.html'

    def get_queryset(self):
        return Cart.objects.get(user=self.request.user)

#
#  CartItem을 생성하는 View
#    - $.post()로 호출
#
@login_required
@cart_ownership
def CartItemCreateView(request):
    if request.method == 'POST':
        user = request.user
        product_id = request.POST.get('product_id', None)
        option_1 = request.POST.get('option_1', None)
        option_2 = request.POST.get('option_2', None)
        quantity = request.POST.get('quantity', 0)
        try:
            cart = Cart.objects.get(user=user)
            product = Product.objects.get(pk=product_id)
            product_option = product.product_option.first()

            # 해당 상품이 이미 장바구니에 있다면
            cart_item = CartItem.objects.filter(cart=cart, product=product)
            if cart_item:
                cart_item.update(quantity=cart_item.first().quantity + 1)  # 수량을 1 증가시킴
            else:
                # 새로운 CartItem object 생성
                new_item = CartItem(
                    cart=cart,
                    product=product,
                    product_option_1=option_1,
                    product_option_2=option_2,
                    quantity=quantity
                )
                new_item.save()

            return HttpResponse(status=200)

        except ObjectDoesNotExist:
            print('잘못된 장바구니 또는 상품 조회!')
            return HttpResponse(status=500)


@login_required
@cart_ownership
def CartItemDeleteView(request, cart_pk):
    if request.method == 'POST':
        target_cart = Cart.objects.get(pk=cart_pk)
        cart_item_list = request.POST.getlist('cart_item_list[]', None)

        try:
            for item_pk in cart_item_list:
                cart_item = target_cart.cart_item.get(pk=item_pk)
                cart_item.delete()
            return HttpResponse(status=200)

        except ObjectDoesNotExist:
            print('잘못된 장바구니 상품 조회!')
            return HttpResponse(status=500)


@login_required
@cart_ownership
def CartItemQuantityUpdateView(request, cart_pk):
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(pk=cart_pk)
            cart.cart_item.filter(pk=request.POST.get('target_item')).update(quantity=request.POST.get('input_quantity'))
            return HttpResponse(status=200)

        except ObjectDoesNotExist:
            print('잘못된 장바구니 상품 조회!')
            return HttpResponse(status=500)
