from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from productapp.forms import ProductCreationForm, ProductThumbnailCreationForm
from productapp.models import Product


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreationForm
    template_name = 'productapp/create.html'

    def form_valid(self, form):
        new_item = form.save(commit=False)
        print(new_item)


class ProductCreateThumbnailView(CreateView):
    model = Product
    form_class = ProductThumbnailCreationForm
    template_name = 'productapp/snippets/upload_thumbnail.html'


