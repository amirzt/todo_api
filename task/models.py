from django.db import models

from user.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255, null=False)

    is_global = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=255, null=False)
    due_date = models.DateField(null=True)
    due_time = models.TimeField(null=True)

    is_starred = models.BooleanField(default=False)

    status = models.BooleanField(default=False)

    note = models.TextField(null=True, max_length=1000)
    color = models.CharField(max_length=255, null=True, default='#ffffff')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    title = models.CharField(max_length=255, null=False)
    status = models.BooleanField(default=False)
    # order = models.AutoField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    time = models.TimeField(null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Attachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    file = models.FileField(upload_to='attachments/', null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

