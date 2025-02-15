from django.db import models

# Create your models here.

class TodoList(models.Model):
    name = models.CharField(max_length=200)

class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="todos")