from django.contrib import admin

# Register your models here.
from addressapp.models import UserAddress

admin.site.register(UserAddress)