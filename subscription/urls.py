from django.urls import path
from .import views as my_views

urlpatterns = [
    path('add-supscription/', my_views.add_subscription, name='add-supscription'),
    path('subscrip/', my_views.sub_scription_view, name='subscrip-url'),
]