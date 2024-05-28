from django.urls import path
from .views import search_view, search_form_view, blog_post_details_view

app_name = 'search'

urlpatterns = [
    path('api/search/', search_view, name='search'),
    path('form/', search_form_view, name='search_form'),
    path('api/blog/<int:post_id>/', blog_post_details_view, name='blog_post_details'),
    path('api/search/blog-posts/', api_search_blog_posts_view, name='api_search_blog_posts'),
]
