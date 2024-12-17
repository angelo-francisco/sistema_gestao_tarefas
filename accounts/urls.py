from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from .views import SignupView, LoginView


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
        LogoutView.as_view(
            template_name="registration/logout.html",
            next_page=reverse_lazy("login"),
        ),
        name="logout",
    ),
]
