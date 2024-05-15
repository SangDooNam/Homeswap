from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogPostSerializer
from blog.models import BlogPost
from accounts.models import AppUser

@api_view(['GET'])
def search_view(request):
    if not request.user.is_authenticated:
        return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

    user_location = request.user.location
    search_destination = request.query_params.get('search_destination')
    search_start_date = request.query_params.get('search_start_date')
    search_end_date = request.query_params.get('search_end_date')
    search_num_travelers = request.query_params.get('search_num_travelers')

    blog_posts = BlogPost.objects.filter(
        to_city=user_location,  
        location=search_destination,
        start_date__lte=search_start_date,
        end_date__gte=search_end_date,
        max_capacity__gte=search_num_travelers,
    )

    serializer = BlogPostSerializer(blog_posts, many=True)
    return render(request, 'search.html', {'blog_posts': serializer.data})