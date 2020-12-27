from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from accountapp.models import User


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    readonly_fields = ['created_at']

    list_display = ['email', 'username', 'created_at', 'is_active', 'is_admin']
    list_filter = ['is_admin', 'is_active']
    fieldsets = [
        ['default_info', {'fields': ['email', 'username', 'created_at']}],
        ['extra_info', {'fields': ['phone_number', 'date_of_birth']}],
        ['permissions', {'fields': ['is_active', 'is_admin']}]
    ]

    add_fieldsets = [
        [None, {'classes': ['wide'],
                'fields': ['email', 'username', 'password1', 'password2', 'phone_number', 'date_of_birth']
                }]
    ]

    filter_horizontal = []

# 직접 생성한 Custom User Manager와 관리자 폼을 사용하도록 등록
admin.site.register(User, UserAdmin)

# 장고에서 기본적으로 제공하는 Group은 사용하지 않도록 설정
admin.site.unregister(Group)