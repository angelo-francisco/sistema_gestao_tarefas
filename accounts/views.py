import random
import string

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView as LoginViewDjango
from django.contrib.auth.views import LogoutView as LogoutViewDjango
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.edit import FormView

from .forms import ForgotPasswordForm, SignupForm, VerifyCodeForm
from .models import PasswordResetCode
from .tasks import email_user_reset_password

force_text = force_str


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

                if form.cleaned_data.get("reset_method") == "code":
                    email_user_reset_password.delay(
                        email=user.email, by="code", code=code
                    )
                    PasswordResetCode.objects.create(user=user, code=code)
                    messages.success(request, "Reset password code sent.")
                    return redirect("verify_code")
                else:
                    uuid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)

                    link = request.build_absolute_uri(
                        reverse(
                            "reset_password_by_email",
                            kwargs={
                                "uuid": uuid,
                                "token": token
                            }
                        )
                    )
                    
                    email_user_reset_password.delay(
                        email=user.email,
                        by="email",
                        link=link
                    )
                    messages.success(request, "Link sent to your email.")
                    return redirect("forgot_password")

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
    return render(request, "registration/reset_password.html", ctx)


def reset_password_by_email(request, uuid, token):
    ctx = {}
    pk = force_text(urlsafe_base64_decode(uuid))

    user = get_object_or_404(User, pk=pk)

    if not default_token_generator.check_token(user, token):
        messages.error(request, 'Invalid Token, try again later with new link')
        return redirect(reverse("forgot_password"))

    if request.method == "POST":
        form = SetPasswordForm(user=user, data=request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Password Reseted!")
            return redirect("login")
    else:
        form = SetPasswordForm(user=user)
    
    ctx["form"] = form
    return render(request, "registration/reset_password.html", ctx)
