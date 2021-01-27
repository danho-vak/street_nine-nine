from django.forms import ModelForm

from cartapp.models import Cart, CartItem


class CartItemCreationForm(ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        exclude = ['cart', 'product', 'product_option']