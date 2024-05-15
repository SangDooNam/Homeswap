from django.urls import path
from .views import BlogListView, BlogPostView, blog_post_details

app_name = 'blog'

urlpatterns = [
    path('create/', BlogPostView.as_view(), name='create_blog'),
    path('', BlogListView.as_view(), name='home'),
    path('details/<int:post_id>/', blog_post_details, name='blog_post_details'), 
]
