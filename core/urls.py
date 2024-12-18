from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("accounts.urls")),
    path("task/", include('tasks.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


handler404 = "tasks.views.handler404"