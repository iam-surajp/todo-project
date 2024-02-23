from django.forms import ModelForm

from .models import Tasks


class todo_task(ModelForm):
    class Meta:
        model = Tasks
        fields = ['title','desc','important']