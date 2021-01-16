from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, DetailView

from productapp.models import Product


# def tempview(request):
#     return render(request, 'storeapp/index.html')


class StoreMainList(ListView):
    model = Product
    context_object_name = 'product_list'
    template_name = 'storeapp/main/index.html'

    def get_queryset(self):
        return Product.objects.all().select_related().order_by('-product_created_at')
