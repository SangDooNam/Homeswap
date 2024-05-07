from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('', views.blog_post_list, name='blog_post_list'),
]
