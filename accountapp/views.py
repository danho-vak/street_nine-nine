
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from accountapp.forms import CustomUserCreationForm
from accountapp.models import User


class AccountLoginView(LoginView):
    template_name = 'accountapp/login.html'


class AccountCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accountapp/create.html'


class AccountLogOutView(LogoutView):
    pass