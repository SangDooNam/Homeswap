from django.forms import BaseModelForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet, Q
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse, Http404
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.core.exceptions import PermissionDenied

from typing import Any
from .models import AppUser, HomePhoto
from .forms import RegistrationForm, ProfileForm, HomePhotoForm #HomePhotoFormSet
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
    success_url = reverse_lazy('accounts:profile')
    
    def get_form_class(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to upload photos.")
        current_photos_count = HomePhoto.objects.filter(user=self.request.user).count()
        max_photos = 10
        self.left_amount = max_photos-current_photos_count
        self.extra_forms = min(3, self.left_amount)
        return modelformset_factory(HomePhoto, HomePhotoForm, extra=self.extra_forms, max_num=max_photos, fields=['image', 'photo_type'])
    
    def get_object(self, queryset: QuerySet[reverse_lazy] | None = ...) -> Model:
        if self.request.user.is_authenticated:
            self.object = self.request.user
        else:
            raise Http404("User must be authenticated")
        return self.object
    
    def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
        if not hasattr(self, 'object'):
            self.get_object()
        context =  super().get_context_data(**kwargs)
        FormClass = self.get_form_class()
        if 'form' not in context:
            context['form'] = FormClass(queryset=HomePhoto.objects.none())
        
        photos = HomePhoto.objects.filter(user=self.request.user)
        context['photos'] = photos
        context['extra_num'] = self.extra_forms
        context['left_amount'] = self.left_amount
        
        return context
    
    def post(self, request, *args, **kwargs):
        FormClass = self.get_form_class()
        formset = FormClass(request.POST, request.FILES, queryset=HomePhoto.objects.none())
        
        if formset.is_valid() and request.FILES:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.user = request.user
                instance.save()
            formset.save()
            print('this', request.POST)
            print(request.FILES)
            #print('Formset saved successfully.')
            return HttpResponseRedirect(self.success_url)
        else:
            #print('Formset is invalid:', formset.errors)
            return self.form_invalid(formset)
    
    def form_invalid(self, formset):
        context = self.get_context_data(form=formset)
        return self.render_to_response(context)


class ProfileEditView(UpdateView):
    
    form_class = ProfileForm
    template_name = "main/edit_profile.html"
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset: QuerySet[reverse_lazy] | None = ...) -> Model:
        try:
            if self.request.user.is_authenticated:
                return self.request.user
        except self.request.user.DoesNotExist as error:
            raise error
        
        
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if self.request.user.is_authenticated:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


def delete_image(request, pk):
    
    user = request.user
    try:
        image_to_delete = HomePhoto.objects.get(pk=pk, user=user)
        image_to_delete.delete()
        return redirect(reverse('accounts:profile'))
    except HomePhoto.DoesNotExist:
        raise HttpResponse("Image not found", status=400)

