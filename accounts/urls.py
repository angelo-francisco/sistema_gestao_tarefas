from django.urls import path, reverse_lazy

from .views import (
    LoginView,
    LogoutView,
    SignupView,
    forgot_password,
    reset_password_by_code,
    verify_code,
    reset_password_by_email
)


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="registration/login.html",
            next_page=reverse_lazy("task_list_view"),
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "signup/",
        SignupView.as_view(template_name="registration/signup.html"),
        name="signup",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path("forgot_password/", forgot_password, name="forgot_password"),
    path("verify_code/", verify_code, name="verify_code"),
    path(
        "reset_password_by_code/<code_hash>/",
        reset_password_by_code,
        name="reset_password_by_code",
    ),
    path(
        "reset_password_by_email/<uuid>/<token>/",
        reset_password_by_email,
        name="reset_password_by_email"
    )
]
