import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from .forms import TaskForm
from .models import Task

logger = logging.getLogger(__name__)

only_logged_users = login_required(login_url=settings.LOGIN_URL)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Task.objects.filter(user=self.request.user)
        return queryset


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("task_list_view")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user

        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy("task_list_view")

    def get_object(self, queryset=None):
        uid = self.kwargs.get("uid")
        return Task.objects.get(uid=uid)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    after_submit_form = reverse_lazy("task_detail_view")

    def get_after_submit_form_url(self):
        return self.after_submit_form

    def get_object(self, queryset=None):
        uid = self.kwargs.get("uid")
        return Task.objects.get(uid=uid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        task = self.get_object()
        context["form"] = TaskForm(instance=task)
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("task_detail_view", uid=task.uid)
        return self.render_to_response(self.get_context_data(form=form))


@csrf_exempt
def check_task(request, uid):
    ctx = {}
    task = get_object_or_404(Task, uid=uid)

    if request.method == "POST":
        task.status = False if task.status else True
        task.save()

    ctx["tasks"] = Task.objects.filter(user=request.user)
    return render(request, "partials/task_cards.html", ctx)


def handler404(request, exception):
    return render(request, "erros/404.html")