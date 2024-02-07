from django.urls import path
from . import views as my_views

urlpatterns = [
    path('register/', my_views.registration_view, name='register-url'),
    path('logout/', my_views.logout_view, name='logout-url'),
    path('login/', my_views.login_view, name='login-url'),
    path('profile/', my_views.account_view, name='profile-url'),
    path('authenticate/', my_views.must_authenticate, name='authenticate-url')
]