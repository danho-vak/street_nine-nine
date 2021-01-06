from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView

from accountapp.forms import CustomUserCreationForm
from accountapp.models import User


class AccountCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('accountapp:login')


class AccountPWChangeView(FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'accountapp/pw_update.html'

    def get_form_kwargs(self):
        kwargs = super(AccountPWChangeView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        if self.request.method == 'POST':
            kwargs['data'] = self.request.POST
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        return super(AccountPWChangeView, self).form_valid(form)

    def get_success_url(self):
        return reverse('accountapp:profile', kwargs={'pk' : self.request.user.pk})


class AccountProfileView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/profile.html'

    # 다른 user가 접근 못하게 설정
    def get(self, request, *args, **kwargs):
        if request.user == User.objects.get(pk=self.kwargs['pk']):
            return super(AccountProfileView, self).get(request, *args, **kwargs)
        else:
            return redirect('storeapp:index')


class AccountProfileDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'

    # 다른 user가 접근 못하게 설정
    def get(self, request, *args, **kwargs):
        if request.user == User.objects.get(pk=self.kwargs['pk']):
            return super(AccountProfileDetailView, self).get(request, *args, **kwargs)
        else:
            return redirect('storeapp:index')


class AccountLoginView(LoginView):
    template_name = 'accountapp/login.html'


class AccountLogOutView(LogoutView):
    pass
