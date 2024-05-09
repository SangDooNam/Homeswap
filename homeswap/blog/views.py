from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView
from django.urls import reverse, reverse_lazy

from typing import Any
from .forms import BlogPostForm
from .models import BlogPost
from accounts.models import HomePhoto

# @login_required
# def create_blog_post(request):
#     if request.method == 'POST':
#         form = BlogPostForm(request.POST)
#         if form.is_valid():
#             blog_post = form.save(commit=False)
#             blog_post.user = request.user
#             blog_post.save()


#             return redirect('blog_home')  
        
#     else:
#         form = BlogPostForm()
#     return render(request, 'blog/create_blog_post.html', {'form': form})


# def blog_post_list(request):
#     blog_posts = BlogPost.objects.all()
#     return render(request, 'blog/blog_post_list.html', {'blog_posts': blog_posts})


class BlogView(TemplateView):
    
    template_name = 'blog_post_list.html'
    


class BlogPostView(FormView):
    
    template_name = 'create_blog_post.html'
    form_class = BlogPostForm
    success_url = reverse_lazy('blog:home')
    
    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            
            photos = HomePhoto.objects.filter(user=self.request.user)
            
            context['photos'] = photos
            
            return context
        
    def form_valid(self, form):
        blog_post = form.save(commit=False)
        blog_post.user = self.request.user
        blog_post.save()
        return super().form_valid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        return super().form_invalid(form)