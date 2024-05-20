from django.urls import path
from .views import BlogListView, BlogPostView, delete_blog

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('create/', BlogPostView.as_view(), name='create_blog'),
    path('delete/<int:pk>', delete_blog, name='delete_blog'),
]
