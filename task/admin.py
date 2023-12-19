from django.contrib import admin

# Register your models here.
from task.models import Category, Task, SubTask, Reminder, Attachment

admin.site.register(Category)
admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Reminder)
admin.site.register(Attachment)
