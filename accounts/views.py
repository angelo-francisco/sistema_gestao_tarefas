from django.shortcuts import render #noqa
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView as LoginViewDjango
from django.contrib.auth.views import LogoutView as LogoutViewDjango
from django.http import HttpResponseRedirect
from django.conf import settings


class SignupView(FormView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):

        return super().form_invalid(form)
    

class LoginView(LoginViewDjango):
    ...
    
class LogoutView(LogoutViewDjango):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)