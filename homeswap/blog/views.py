from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from accounts.models import HomePhoto

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()

            user_home_photos = HomePhoto.objects.filter(user=request.user)
            blog_post.home_photos.set(user_home_photos)

            return redirect('blog_home')  
        
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blog_post.html', {'form': form})
