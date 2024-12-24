from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("auth/", include("accounts.urls"), name="accounts"),
    path("task/", include("tasks.urls"), name="tasks"),
    path("", RedirectView.as_view(url=reverse_lazy("task_list_view"))),
]


handler404 = "tasks.views.handler404"
