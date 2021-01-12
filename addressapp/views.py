from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import FormMixin

from addressapp.forms import AddressCreationForm
from addressapp.models import UserAddress


@method_decorator(login_required, 'dispatch')
class AddressCreateView(CreateView):
    model = UserAddress
    form_class = AddressCreationForm
    template_name = 'addressapp/create.html'
    success_url = reverse_lazy('addressapp:list')

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.target_user = self.request.user
        new_item.is_default = set_default_address(self.request)  # 아래 set_default_address()에서 반환된 bool값을 저장
        new_item.save()
        return super().form_valid(form)


@method_decorator(login_required, 'get')
class AddressListView(ListView, FormMixin):
    template_name = 'addressapp/list.html'
    context_object_name = 'address_list'
    form_class = AddressCreationForm

    def get_queryset(self):
        return UserAddress.objects.filter(target_user=self.request.user)


# 주소를 수정하는 로직 말고 주소의 기본값 설정을 바꾸는 쪽으로 생각해보자
@method_decorator(login_required, 'dispatch')
class AddressUpdateDefaultView(UpdateView):
    model = UserAddress
    form_class = AddressCreationForm
    success_url = reverse_lazy('addressapp:list')

    def form_valid(self, form):
        update_item = form.save(commit=False)
        update_item.is_default = set_default_address(self.request)
        update_item.save()
        return super().form_valid(form)


@method_decorator(login_required, 'dispatch')
class AddressDeleteView(DeleteView):
    model = UserAddress
    pass


'''
    기본 배송지로 설정하는 함수
    
'''
def set_default_address(request):
    # 기존에 기본 주소로 설정되어 있는 레코드 탐색
    before_object = UserAddress.objects.filter(target_user=request.user, is_default=True)

    if before_object:  # 탐색된 레코드가 있다면
        if request.POST.get('is_default', None) == 'checked':  # 기본 주소 설정 체크박스가 체크되었다면
            before_object.update(is_default=False)  # 해당 레코드의 기본 주소 설정 값을 False로 변경하고 True 반환
            return True
        else:
            return False
    else:
        return True  # 탐색된 레코드가 없다면(최초 등록의 경우) True 반환
