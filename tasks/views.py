from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView

from .forms import TaskForm
from .models import Task


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

    def get_success_url(self):
        return reverse("task_list_view")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user

        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def get_success_url(self):
        success_url = reverse("task_list_view")
        return success_url

    def get_object(self, queryset=None):
        uid = self.kwargs.get("uid")
        return Task.objects.get(uid=uid)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())


@login_required
def TaskDetailView(request, uid):
    ctx = {}
    template_name = "tasks/task_detail.html"
    task = Task.objects.get(uid=uid)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            
            return redirect("task_detail_view", uid=task.uid)
    else:
        form = TaskForm(instance=task)

    ctx["form"] = form
    ctx["object"] = task
    return render(request, template_name, ctx)


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
