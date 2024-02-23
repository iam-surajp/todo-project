from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tasks(models.Model):
    title = models.CharField(max_length=300)
    desc = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
