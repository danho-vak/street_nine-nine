from django.urls import path

from reviewapp.views import ReviewCreateView

app_name = 'reviewapp'

urlpatterns = [
    path('create/', ReviewCreateView.as_view(), name='create'),
]