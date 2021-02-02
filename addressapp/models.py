from django.db import models

from accountapp.models import User


class UserAddress(models.Model):
    target_user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_alias = models.CharField(max_length=25, null=False, blank=False)
    address_lot_number = models.CharField(max_length=120, null=False)  # 지번
    address_road_name = models.CharField(max_length=120, null=False)  # 도로명
    address_detail_info = models.CharField(max_length=30, null=True, blank=True, default='')
    zip_code = models.CharField(max_length=8, null=False)
    is_default = models.BooleanField(default=False, null=True, blank=True)  # 기본 주소 설정 여부

    def __str__(self):
        if self.is_default:
            return '{} > {} (default)'.format(self.target_user, self.address_alias)
        else:
            return '{} > {}'.format(self.target_user.username, self.address_alias)
