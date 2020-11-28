from django.db import models

# Create your models here.


class TaskList(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
