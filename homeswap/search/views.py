from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogPostSerializer, HomePhotoSerializer
from blog.models import BlogPost
from accounts.models import AppUser, HomePhoto
from datetime import datetime

def search_form_view(request):
    return render(request, 'search/search_form.html')

@api_view(['GET'])
def search_view(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    user_location = request.user.location
    search_destination = request.query_params.get('search_destination')
    search_start_date = request.query_params.get('search_start_date')
    search_end_date = request.query_params.get('search_end_date')
    search_num_travelers = request.query_params.get('search_num_travelers')

    if not all([search_destination, search_start_date, search_end_date, search_num_travelers]):
        return Response({"error": "All search parameters must be provided."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        search_start_date = datetime.strptime(search_start_date, '%Y-%m-%d')
        search_end_date = datetime.strptime(search_end_date, '%Y-%m-%d')
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        search_num_travelers = int(search_num_travelers)
    except ValueError:
        return Response({"error": "search_num_travelers must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

    blog_posts = BlogPost.objects.filter(
        to_city=user_location,
        location=search_destination,
        start_date__lte=search_start_date,
        end_date__gte=search_end_date,
        max_capacity__gte=search_num_travelers,
    )

    serializer = BlogPostSerializer(blog_posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def blog_post_details_view(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    photos = HomePhoto.objects.filter(user=blog_post.user)
    
    data = {
        'title': blog_post.title,
        'description': blog_post.description,
        'location': blog_post.location,
        'to_city': blog_post.to_city,
        'max_capacity': blog_post.max_capacity,
        'start_date': blog_post.start_date,
        'end_date': blog_post.end_date,
        'user_photos': [{'image_url': photo.image.url, 'photo_type': photo.photo_type} for photo in photos]
    }
    
    return Response(data, status=status.HTTP_200_OK)