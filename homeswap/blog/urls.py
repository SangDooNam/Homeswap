from django.urls import path
from .views import BlogListView, BlogPostCreateView, delete_blog, BlogPostUpdateView, CheckBlogPost

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('create/', BlogPostCreateView.as_view(), name='create_blog'),
    path('check/', CheckBlogPost.as_view(), name="check_blog"),
    path('delete/<int:pk>', delete_blog, name='delete_blog'),
    path('edit/<int:pk>', BlogPostUpdateView.as_view(), name='edit'),
]
