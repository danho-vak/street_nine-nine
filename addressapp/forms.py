from django.forms import ModelForm

from addressapp.models import UserAddress


class AddressCreationForm(ModelForm):
    class Meta:
        model = UserAddress
        fields = ['address_alias', 'address_lot_number', 'address_road_name', 'zip_code', 'is_default']
        exclude = ['target_user']