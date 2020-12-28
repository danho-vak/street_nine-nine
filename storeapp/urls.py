from django.urls import path

from storeapp.views import tempview

app_name = 'storeapp'


urlpatterns = [
    path('', tempview, name='index')
]