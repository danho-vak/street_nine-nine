from django.db import models

from accountapp.models import User


class UserAddress(models.Model):
    target_user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_alias = models.CharField(max_length=25, null=False, blank=False)
    address_lot_number = models.CharField(max_length=120, null=False)  # 지번
    address_road_name = models.CharField(max_length=120, null=False)  # 도로명
    zip_code = models.CharField(max_length=8, null=False)