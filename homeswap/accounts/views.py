from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from typing import Any
from .forms import RegistrationForm, ProfileForm, LoginForm

# Create your views here.


class LogInView(LoginView):
    
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = ''
    
    def get_success_url(self) -> str:
        return reverse_lazy('')
    
    def dispatch(self, request: HttpRequest, *args: reverse_lazy, **kwargs: reverse_lazy) -> HttpResponse:
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        
        return super().dispatch(request, *args, **kwargs)


class RegistrationView(FormView):
    template_name = ''
    success_url = reverse_lazy('')
    form_class = RegistrationForm
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse(''))