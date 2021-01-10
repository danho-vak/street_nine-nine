from django.urls import path

from storeapp.views import StoreMainList

app_name = 'storeapp'

urlpatterns = [
    path('', StoreMainList.as_view(), name='index'),
]