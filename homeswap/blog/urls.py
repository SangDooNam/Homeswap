from django.urls import path
<<<<<<< HEAD


app_name = 'blog'

urlpatterns = [
    
]
=======
from . import views

urlpatterns = [
    path('create/', views.create_blog_post, name='create_blog_post'),
    path('', views.blog_post_list, name='blog_post_list'),
]
>>>>>>> origin/app/blog
