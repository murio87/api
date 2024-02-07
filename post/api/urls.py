from django.urls import path
from post.api.views import api_get_view, api_update_view, api_delete_view, api_create_view, ApiBlogView

app_name = 'post'

urlpatterns = [
    path('<slug>/', api_get_view, name='detail'),
    path('<slug>/update', api_update_view, name='update'),
    path('<slug>/delete', api_delete_view, name='delete'),
    path('create', api_create_view, name='create'),
    path('list', ApiBlogView.as_view(), name='list'),
]