from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView
from django.http import Http404

from typing import Any
from .forms import BlogPostForm
from .models import BlogPost
from accounts.models import HomePhoto
from accounts.views import get_or_none
from search.forms import BlogPostSearchForm


class BlogListView(ListView):
    
    model = BlogPost
    template_name = 'blog_post_list.html'
    context_object_name = 'blog_posts'
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        
        queryset = BlogPost.objects.all()
        
        return queryset
    
    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = BlogPostSearchForm()
        
        return context

class BlogPostCreateView(FormView):
    
    template_name = 'create_blog_post.html'
    form_class = BlogPostForm
    success_url = reverse_lazy('blog:check_blog')
    
    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)
            
            photos = HomePhoto.objects.filter(user=self.request.user)
            
            context['photos'] = photos
            
            return context
        else:
            raise PermissionDenied("You must be logged in.")
    
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


def delete_blog(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        
        delete_obj = get_object_or_404(BlogPost, pk=pk, user=request.user)
        delete_obj.delete()
        return redirect('accounts:profile')
    else:
        raise HttpResponse("Invalid request", status=400)


class CheckBlogPost(TemplateView):
    template_name = "partials/check_individual_post.html"

    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        individual_post = get_or_none(BlogPost, user=self.request.user)
        context['individual_post'] = individual_post
        return context


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "partials/blogpost_update.html"
    success_url = reverse_lazy('blog:check_blog')

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.get('pk', None)
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        
        obj = super().get_object(queryset)
        
        if obj.user != self.request.user:
            raise Http404("You do not have permission to access this object")
        return obj

    def get_queryset(self):
        return BlogPost.objects.filter(pk=self.pk)

    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['pk'] = self.pk
        return context
