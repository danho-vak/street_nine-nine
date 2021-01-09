from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from addressapp.forms import AddressCreationForm
from addressapp.models import UserAddress


class AddressCreateView(CreateView):
    model = UserAddress
    form_class = AddressCreationForm
    template_name = 'addressapp/product_create.html'

    success_url = reverse_lazy('storeapp:index')

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.target_user = self.request.user
        new_item.save()

        return super().form_valid(form)


class AddressListView(ListView, FormMixin):
    template_name = 'addressapp/list.html'
    context_object_name = 'address_list'
    form_class = AddressCreationForm

    def get_queryset(self):
        return UserAddress.objects.filter(target_user=self.request.user)


class AddressUpdateView(UpdateView):
    model = UserAddress
    pass


class AddressDeleteView(DeleteView):
    model = UserAddress
    pass