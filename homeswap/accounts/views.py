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

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.sites.shortcuts import get_current_site

from allauth.account.forms import LoginForm, SignupForm
from allauth import app_settings as allauth_app_settings

from allauth.socialaccount.models import SocialAccount
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.forms import (
    AddEmailForm,
    ChangePasswordForm,
    ConfirmLoginCodeForm,
    LoginForm,
    ReauthenticateForm,
    RequestLoginCodeForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordForm,
    SignupForm,
    UserTokenForm,
)
from allauth.account.internal import flows
from allauth.account.mixins import (
    AjaxCapableProcessFormViewMixin,
    CloseableSignupMixin,
    LogoutFunctionalityMixin,
    NextRedirectMixin,
    RedirectAuthenticatedUserMixin,
    _ajax_response,
)
from allauth.account.models import (
    EmailAddress,
    EmailConfirmation,
    get_emailconfirmation_model,
)
from allauth.account.reauthentication import resume_request
from allauth.account.utils import (
    complete_signup,
    perform_login,
    send_email_confirmation,
    sync_user_email_addresses,
    url_str_to_user_pk,
    user_display,
)
from allauth.core import ratelimit
from allauth.core.exceptions import ImmediateHttpResponse
from allauth.core.internal.httpkit import redirect
from allauth.decorators import rate_limit
from allauth.utils import get_form_class

from typing import Any
from .models import AppUser, HomePhoto
from .forms import RegistrationForm, ProfileForm, HomePhotoForm #HomePhotoFormSet


# Create your views here.

# class HomeView(FormView):
    
#     template_name = 'home.html'
#     form_class = LoginForm
    
#     def get_context_data(self, **kwargs: reverse_lazy) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
        
#         signup_form = SignupForm
        
#         context['signup_form'] = signup_form
#         return context


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters("oldpassword", "password", "password1", "password2")
)

class HomeView(
    NextRedirectMixin,
    RedirectAuthenticatedUserMixin,
    AjaxCapableProcessFormViewMixin,
    FormView,
):
    form_class = LoginForm
    template_name = "home.html"
    success_url = None

    @sensitive_post_parameters_m
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if allauth_app_settings.SOCIALACCOUNT_ONLY and request.method != "GET":
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, "login", self.form_class)

    def form_valid(self, form):
        redirect_url = self.get_success_url()
        try:
            return form.login(self.request, redirect_url=redirect_url)
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        signup_url = None
        if not allauth_app_settings.SOCIALACCOUNT_ONLY:
            signup_url = self.passthrough_next_url(reverse("account_signup"))
        site = get_current_site(self.request)

        signup_form = SignupForm
        
        ret['signup_form'] = signup_form
        
        reset_password_form = ResetPasswordForm
        
        ret['reset_password_form'] = reset_password_form
        
        ret.update(
            {
                "signup_url": signup_url,
                "site": site,
                "SOCIALACCOUNT_ENABLED": allauth_app_settings.SOCIALACCOUNT_ENABLED,
                "SOCIALACCOUNT_ONLY": allauth_app_settings.SOCIALACCOUNT_ONLY,
                "LOGIN_BY_CODE_ENABLED": app_settings.LOGIN_BY_CODE_ENABLED,
            }
        )
        if app_settings.LOGIN_BY_CODE_ENABLED:
            request_login_code_url = self.passthrough_next_url(
                reverse("account_request_login_code")
            )
            ret["request_login_code_url"] = request_login_code_url
        return ret


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

class PasswordResetView(TemplateView):
    
    template_name = 'account/password_reset.html'
    
