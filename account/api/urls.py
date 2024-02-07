from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from account.api.views import registration_view, update_account_view, account_properties_view

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name='register'),
    path('login', obtain_auth_token, name='login'),
    path('properties', account_properties_view, name='properties'),
    path('properties/update', update_account_view, name='update'),
]