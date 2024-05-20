from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView
from django.views.generic.detail import DetailView
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView

from typing import Any
from .forms import BlogPostForm
from .models import BlogPost
from accounts.models import HomePhoto


class BlogListView(ListView):
    
    model = BlogPost
    template_name = 'blog_post_list.html'
    context_object_name = 'blog_posts'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        
        queryset = BlogPost.objects.all()
        
        return queryset
    
    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        
        context['blog_posts'] = self.get_object()
        
        return context


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
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
        
    def form_valid(self, form):
        blog_post = form.save(commit=False)
        blog_post.user = self.request.user
        blog_post.location = self.request.user.location
        blog_post.max_capacity = self.request.user.max_capacity
        blog_post.save()
        return super().form_valid(form)
    
    def form_invalid(self, form: Any) -> HttpResponse:
        return super().form_invalid(form)

def delete_blog(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        
        delete_obj = get_object_or_404(BlogPost, pk=pk, user=request.user)
        delete_obj.delete()
        return redirect('accounts:profile')
    else:
        raise HttpResponse("Invalid request", status=400)
    

class BlogPostUpdateView(UpdateView):
    
    form_class = BlogPost
    template_name = ""
    success_url = reverse_lazy('accounts:profile')