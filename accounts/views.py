import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as LoginViewDjango
from django.contrib.auth.views import LogoutView as LogoutViewDjango
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from .forms import ForgotPasswordForm, SignupForm, VerifyCodeForm
from .models import PasswordResetCode


class SignupView(FormView):
    form_class = SignupForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class LoginView(LoginViewDjango): ...


class LogoutView(LoginRequiredMixin, LogoutViewDjango):
    http_method_names = ["post", "get"]
    template_name = ("registration/logout.html",)
    next_page = reverse_lazy("login")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to=settings.LOGIN_URL)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            "user": request.user,
        }
        return render(request, self.template_name, context)


def get_verification_code(length=8):
    characters = string.ascii_uppercase + string.digits
    code = "".join(random.choice(characters) for _ in range(length))

    while PasswordResetCode.objects.filter(code=code).exists():
        code = "".join(random.choice(characters) for _ in range(length))

    return code


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect("task_list_view")

    ctx = {}

    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)

        if form.is_valid():
            user = form.get_user()

            if user is not None:
                code = get_verification_code()
                reset_link = request.build_absolute_uri(reverse_lazy('verify_code'))
                user.email_user(
                    subject="Verification Code",
                    message=f"Use this code {code} in reset password link: {reset_link}",
                    from_email="ics20080729@gmail.com",
                )

                PasswordResetCode.objects.create(user=user, code=code)

                messages.success(request, "Reset password code sent.")
                return redirect("verify_code")

            messages.warning(request, "This code is invalid., try again later.")
            return redirect("forgot_password")
    else:
        form = ForgotPasswordForm()

    ctx["form"] = form
    return render(request, "registration/forgot_password.html", ctx)


def verify_code(request):
    if request.user.is_authenticated:
        return redirect("task_list_view")

    ctx = {}

    if request.method == "POST":
        form = VerifyCodeForm(request.POST)

        if form.is_valid():
            code = form.cleaned_data.get("code")

            password_reset = PasswordResetCode.objects.get(code=code)

            if not password_reset.is_expired():
                password_reset.status = "U"
                password_reset.save()

                messages.success(request, "Code verified!")
                return redirect(
                    "reset_password_by_code", code_hash=password_reset.code_hash
                )
            else:
                password_reset.status = "E"
                password_reset.save()

                messages.info(request, "The code already expired, try again later")
                return redirect("forgot_password")
    else:
        form = VerifyCodeForm()

    ctx["form"] = form
    return render(request, "registration/verify_code.html", ctx)


def reset_password_by_code(request, code_hash):
    if request.user.is_authenticated:
        return redirect("task_list_view")

    ctx = {}
    user = get_object_or_404(PasswordResetCode, code_hash=code_hash).user

    if request.method == "POST":
        form = SetPasswordForm(user=user, data=request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Password Reseted!")
            return redirect("login")
    else:
        form = SetPasswordForm(user=user)

    ctx["form"] = form
    return render(request, "registration/reset_password_by_code.html", ctx)
