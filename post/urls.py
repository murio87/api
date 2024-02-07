from django.urls import path
from . import views as my_views

urlpatterns = [
    path('create/', my_views.create, name='create-url'),
    path('<slug>/', my_views.detail_blog, name='detail-url'),
    path('<slug>/edit', my_views.edit_blog, name='edit-url'),
    path('delete_blog/<slug:slug>/', my_views.delete_blog, name='delete-blog-url'),
]
