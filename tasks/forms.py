from django import forms
from django.utils.timezone import now, datetime
from datetime import timedelta

from .models import Task
from .tasks import email_notification


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "notify_date")
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter task title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 1,
                    "placeholder": "Enter task description",
                }
            ),
            "notify_date": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                    "placeholder": "Select notification date",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title").strip()

        if not title:
            raise forms.ValidationError("Please, write the task title")
        return title

    def clean_notify_date(self):
        notify_date = self.cleaned_data.get("notify_date")

        if notify_date:
            if isinstance(notify_date, str):
                try:
                    notify_date = datetime.fromisoformat(notify_date)
                except ValueError:
                    raise forms.ValidationError("Invalid date format. Please use the correct format.")
            
            if notify_date <= now():
                raise forms.ValidationError("The notification date must be later than the current time.")

            if notify_date < now() + timedelta(seconds=30):
                raise forms.ValidationError("The notification date must be at least 30 seconfs ahead.")
            
            email_notification.apply_async(
                kwargs={'task_uid':self.instance.uid},
                eta=notify_date
            )
            
        return notify_date
