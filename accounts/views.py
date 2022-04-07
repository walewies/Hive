from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from . import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:login")
    template_name = "signup.html"

class MyLoginView(LoginView):
    template_name="login.html"

class ProfileView(TemplateView):
    template_name = "UserProfile.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context['user'] = self.request.user
        return context