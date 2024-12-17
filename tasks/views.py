import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from django.http import HttpResponseRedirect

from .forms import TaskForm
from .models import Task

logger = logging.getLogger(__name__)

only_logged_users = login_required(login_url=settings.LOGIN_URL)


@only_logged_users
def tasksView(request):
    ctx = {}
    tasks = Task.objects.filter(user=request.user)
    form = TaskForm()

    ctx["form"] = form
    ctx["tasks"] = tasks
    return render(request, "tasks/task_view.html", ctx)



class TaskListView(ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Task.objects.filter(user=self.request.user)
        return queryset


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_create.html"
    success_url = reverse_lazy("task_list_view")
    

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        
        return super().form_valid(form)
    


class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy("task_list_view")

    def get_object(self, queryset=None):
        uid = self.kwargs.get('uid')
        return Task.objects.get(uid=uid)
    
    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        self.object.delete()

        return HttpResponseRedirect(self.get_success_url())

    