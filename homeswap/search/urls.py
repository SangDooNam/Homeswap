from django.urls import path
from .views import search_blog_posts

app_name = 'search'

urlpatterns = [
    path('search-blog-posts/', search_blog_posts, name='search_blog_posts'),
]
