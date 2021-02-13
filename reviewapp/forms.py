from django.forms import ModelForm

from reviewapp.models import Review


class ReviewCreationForm(ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'product_rate']
        exclude = ['user', 'product']
