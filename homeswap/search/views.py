from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogPostSerializer, HomePhotoSerializer
from blog.models import BlogPost
from accounts.models import AppUser, HomePhoto
from datetime import datetime
from .forms import BlogPostSearchForm

def search_form_view(request):
    form = BlogPostSearchForm()
    return render(request, 'search/search_form.html', {'form': form, 'blog_posts': None})

def search_view(request):
    blog_posts = None
    if request.method == 'GET' and 'search_destination' in request.GET:
        form = BlogPostSearchForm(request.GET)
        if form.is_valid():
            if request.user.is_authenticated:
                user_location = request.user.location

                search_destination = form.cleaned_data['search_destination']
                search_start_date = form.cleaned_data['search_start_date']
                search_end_date = form.cleaned_data['search_end_date']
                search_num_travelers = form.cleaned_data['search_num_travelers']

                blog_posts = BlogPost.objects.filter(
                    to_city=user_location,
                    location=search_destination,
                    start_date__lte=search_start_date,
                    end_date__gte=search_end_date,
                    max_capacity__gte=search_num_travelers,
                )
            else:
                return render(request, 'search/search_form.html', {
                    'form': form,
                    'error_message': 'Authentication credentials were not provided.',
                    'blog_posts': None,
                })
        else:
            form = BlogPostSearchForm()
    else:
        form = BlogPostSearchForm()

    return render(request, 'search/search_form.html', {'form': form, 'blog_posts': blog_posts})


@api_view(['GET'])
def blog_post_details_view(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    user_photos = HomePhoto.objects.filter(user=blog_post.user)

    print("User Photos:", user_photos)  # Debug statement to check user_photos

    context = {
        'blog_post': blog_post,
        'user_photos': user_photos
    }

    return render(request, 'search/blog_post_details.html', context)