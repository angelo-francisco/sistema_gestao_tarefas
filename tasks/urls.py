from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    check_task
)


urlpatterns = [
    path("list/", TaskListView.as_view(), name="task_list_view"),
    path("create/", TaskCreateView.as_view(), name="task_create_view"),
    path("delete/<uuid:uid>", TaskDeleteView.as_view(), name="task_delete_view"),
    path("detail/<uuid:uid>", TaskDetailView, name="task_detail_view"),
    path("check/<uuid:uid>", check_task, name="check_task")
]