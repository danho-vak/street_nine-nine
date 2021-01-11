from django.urls import path

from addressapp.views import AddressCreateView, AddressListView

app_name = 'addressapp'


urlpatterns = [
    path('create/', AddressCreateView.as_view(), name='create'),
    path('list/', AddressListView.as_view(), name='list'),
]