from django.urls import path

from accountapp.views import AccountLoginView, AccountLogOutView, AccountCreateView

app_name = 'accountapp'

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogOutView.as_view(), name='logout'),
    path('create/', AccountCreateView.as_view(), name='create'),

]