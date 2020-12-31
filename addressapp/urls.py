from django.urls import path

from addressapp.views import AddressCreateView, AddressListView

app_name = 'addressapp'


urlpatterns = [
    path('list/', AddressListView.as_view(), name='list'),
    path('create/', AddressCreateView.as_view(), name='create'),
]