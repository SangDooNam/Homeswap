from django.urls import path
from .views import BlogListView, BlogPostView

app_name = 'blog'

urlpatterns = [
    path('create/', BlogPostView.as_view(), name='create_blog'),
    path('', BlogListView.as_view(), name='home'),
]
