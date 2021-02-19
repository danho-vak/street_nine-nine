from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect

from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, FormView

from accountapp.decorator import account_has_ownership
from accountapp.forms import CustomUserCreationForm
from accountapp.models import User

from cartapp.models import Cart

# method_decorator로 설정할 user의 인증 여부
USER_HAS_OWNERSHIP = [account_has_ownership, login_required]


class AccountCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('accountapp:login')
    
    def form_valid(self, form):
        user = form.save()
        cart = Cart(user=user)
        cart.save()  # 유저를 생성할 때, 장바구니도 생성
        return super(AccountCreateView, self).form_valid(form) 


@method_decorator(USER_HAS_OWNERSHIP, 'dispatch')
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


@method_decorator(USER_HAS_OWNERSHIP, 'dispatch')
class AccountProfileView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/profile.html'


@method_decorator(USER_HAS_OWNERSHIP, 'dispatch')
class AccountProfileDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'


class AccountLoginView(LoginView):
    template_name = 'accountapp/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # 이미 로그인 되어있다면
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return super().get(request, *args, **kwargs)
