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
from django.contrib.auth.decorators import login_required

from typing import Any
from .models import AppUser
from .forms import RegistrationForm, ProfileForm, LoginForm
import logging
logger = logging.getLogger(__name__)


# Create your views here.

def some_view_before_oauth(request):
    state = request.session.get('some_state_key', 'No state set')
    logger.debug(f"State before initiating OAuth: {state}")
    
    # Possibly doing some setup or showing a page with a "Login with Facebook" button
    return render(request, 'main/logging.html')

class HomeView(TemplateView):
    
    template_name = 'main/home.html'
    


class LogInView(LoginView):
    
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'main/login.html'
    
    def get_success_url(self) -> str:
        if self.request.user.is_admin:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('user_dashboard')
    
    def dispatch(self, request: HttpRequest, *args: reverse_lazy, **kwargs: reverse_lazy) -> HttpResponse:
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        
        return super().dispatch(request, *args, **kwargs)


class RegistrationView(FormView):
    template_name = 'main/registration.html'
    success_url = reverse_lazy('accounts:home')
    form_class = RegistrationForm
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse('accounts:home'))


class ProfileView(DetailView):
    model = AppUser
    template_name = 'main/profile.html'
    context_object_name = 'profile'
    
    