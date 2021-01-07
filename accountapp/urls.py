from django.contrib.auth.views import LogoutView
from django.urls import path

from accountapp.views import AccountProfileView, AccountLoginView, AccountCreateView, \
    AccountPWChangeView, AccountProfileDetailView

app_name = 'accountapp'

urlpatterns = [
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('create/', AccountCreateView.as_view(), name='create'),
    path('profile/<int:pk>/', AccountProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/detail/', AccountProfileDetailView.as_view(), name='detail'),
    path('<int:pk>/changePassword/', AccountPWChangeView.as_view(), name='changePassword'),
]