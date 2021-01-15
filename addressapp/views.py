from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin

from addressapp.forms import AddressCreationForm, AddressDefaultUpdateFrom
from addressapp.models import UserAddress

#
# 배송지를 추가하는 View
#   - form_valid()를 통해 UserAddress Model의 FK를 주입하고
#     is_default field를 set_default_address()를 호출해 설정함
#
@method_decorator(login_required, 'dispatch')
class AddressCreateView(CreateView):
    model = UserAddress
    form_class = AddressCreationForm
    template_name = 'addressapp/create.html'
    success_url = reverse_lazy('addressapp:list')

    def form_valid(self, form):
        new_item = form.save(commit=False)
        new_item.target_user = self.request.user
        new_item.is_default = set_default_address(self.request, 'create')  # 아래 set_default_address()에서 반환된 bool값을 저장
        new_item.save()
        return super().form_valid(form)

#
# 배송지 목록을 뿌려주는 View
#   - get_queryset()으로 request를 보낸 user의 배송지를 가져옴
#
@method_decorator(login_required, 'get')
class AddressListView(ListView, FormMixin):
    template_name = 'addressapp/list.html'
    context_object_name = 'address_list'
    form_class = AddressCreationForm

    def get_queryset(self):
        return UserAddress.objects.filter(target_user=self.request.user)


#
# 기본 배송지로 설정하는 view (addressapp:list에서 ajax로 호출)
#    - post()를 오버라이딩해 요청을 처리하는데 set_default_address()에서 is_default field를 설정함
#
@method_decorator(login_required, 'dispatch')
class AddressUpdateDefaultView(UpdateView):
    def post(self, request, *args, **kwargs):
        set_default_address(self.request, 'update')
        return redirect('addressapp:list')


#
# 배송지를 삭제하는 view (addressapp:list에서 ajax로 호출)
#
@method_decorator(login_required, 'dispatch')
class AddressDeleteView(DeleteView):
    model = UserAddress
    success_url = reverse_lazy('addressapp:list')


#
# 기본 배송지로 설정하는 함수
#   - param : request = requet를 받음
#             case = 어떤 로직을 실행 할지 선택하는 trigger (create, update)
#
def set_default_address(request, case):
    # 기존에 기본 주소로 설정되어 있는 레코드 탐색
    before_object = UserAddress.objects.filter(target_user=request.user, is_default=True)

    if before_object:  # 탐색된 레코드가 있다면
        if case == 'create':
            if request.POST.get('is_default', None) == 'checked':  # 기본 주소 설정 체크박스가 체크되었다면
                before_object.update(is_default=False)  # 해당 레코드의 기본 주소 설정 값을 False로 변경하고 True 반환
                return True
            else:
                return False

        elif case == 'update':
            target_object = UserAddress.objects.filter(pk=request.POST.get('address_pk'))
            before_object.update(is_default=False)
            target_object.update(is_default=True)
    else:
        return True  # 탐색된 레코드가 없다면(최초 등록의 경우) True 반환
