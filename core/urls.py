from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("auth/", include("accounts.urls"), name="accounts"),
    path("task/", include("tasks.urls"), name="tasks"),
    path("", RedirectView.as_view(url=reverse_lazy("task_list_view"))),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = "tasks.views.handler404"
