from django.urls import path
from .views import BlogView, BlogPostView

app_name = 'blog'

urlpatterns = [
    path('create/', BlogPostView.as_view(), name='create_blog'),
    path('', BlogView.as_view(), name='home'),
]
