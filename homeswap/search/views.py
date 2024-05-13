from django.http import JsonResponse
from blog.models import BlogPost


def search_blog_posts(request):
    max_capacity_filter = request.GET.get('max_capacity')
    from_city_filter = request.GET.get('from_city')
    to_city_filter = request.GET.get('to_city')
    dates_filter = request.GET.get('dates')
    
    blog_posts = BlogPost.objects.all()
    
    if max_capacity_filter:
        blog_posts = blog_posts.filter(max_capacity=max_capacity_filter)
    if from_city_filter:
        blog_posts = blog_posts.filter(from_city=from_city_filter)
    if to_city_filter:
        blog_posts = blog_posts.filter(to_city=to_city_filter)
    if dates_filter:
        blog_posts = blog_posts.filter(date_period=dates_filter)
    
    data = [{'from_city': post.from_city, 'to_city': post.to_city,
             'description': post.description} for post in blog_posts]
    return JsonResponse(data, safe=False)


