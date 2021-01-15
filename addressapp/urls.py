from django.urls import path

from addressapp.views import AddressCreateView, AddressListView, AddressUpdateDefaultView, AddressDeleteView

app_name = 'addressapp'


urlpatterns = [
    path('create/', AddressCreateView.as_view(), name='create'),
    path('list/', AddressListView.as_view(), name='list'),
    path('update/<int:pk>/', AddressUpdateDefaultView.as_view(), name='update'),
    path('delete/<int:pk>/', AddressDeleteView.as_view(), name='delete'),
]