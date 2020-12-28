from django.contrib.auth.forms import UserCreationForm

from accountapp.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'phone_number', 'date_of_birth']
