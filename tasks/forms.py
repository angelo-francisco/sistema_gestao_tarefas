from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("title", "description", "notify_date")
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Enter task title",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", 
                "rows": 1,
                "placeholder": "Enter task description",
            }),
            "notify_date": forms.DateTimeInput(attrs={
                "class": "form-control", 
                "type": "datetime-local",
                "placeholder": "Select notification date",
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title').strip()

        if not title:
            raise forms.ValidationError("Please, write the task title")
        return title
