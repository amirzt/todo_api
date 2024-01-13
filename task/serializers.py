from rest_framework import serializers

from task.models import Category, Task, SubTask, Reminder, Attachment


class GetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    def save(self, **kwargs):
        category = Category(name=self.validated_data['name'],
                            user=self.context['user'])
        category.save()
        return category


class AddSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['title', 'task']

    def save(self, **kwargs):
        subtask = SubTask(title=self.validated_data['title'],
                          task=self.validated_data['task'])
        subtask.save()
        return subtask


class GetSubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


class AddReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['time', 'task']

    def save(self, **kwargs):
        reminder = Reminder(time=self.validated_data['time'],
                            task=self.validated_data['task'])
        reminder.save()
        return reminder


class GetReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'


class AddAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['file', 'task']

    def save(self, **kwargs):
        attachment = Attachment(file=self.validated_data['file'],
                                task=self.validated_data['task'])
        attachment.save()
        return attachment


class GetAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = '__all__'


class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'due_date']

    def save(self, **kwargs):
        task = Task(title=self.validated_data['title'],
                    due_date=self.validated_data['due_date'],
                    user=self.context.get('user'))
        task.save()

        if 'category' in self.context.get('data'):
            task.category = Category.objects.get(id=self.context.get('data')['category'])
        if 'due_date' in self.context.get('data'):
            task.due_date = self.context.get('data')['due_date']
        if 'due_time' in self.context.get('data'):
            task.due_time = self.context.get('data')['due_time']
        if 'note' in self.context.get('data'):
            task.note = self.context.get('data')['note']
        task.save()
        return task


class GetTaskSerializer(serializers.ModelSerializer):
    sub_tasks = serializers.SerializerMethodField('get_sub_tasks')
    reminders = serializers.SerializerMethodField('get_reminders')
    attachments = serializers.SerializerMethodField('get_attachments')

    @staticmethod
    def get_sub_tasks(obj):
        sub_tasks = SubTask.objects.filter(task=obj)
        serializer = GetSubTaskSerializer(sub_tasks, many=True)
        return serializer.data

    @staticmethod
    def get_reminders(obj):
        reminders = Reminder.objects.filter(task=obj)
        serializer = GetReminderSerializer(reminders, many=True)
        return serializer.data

    @staticmethod
    def get_attachments(obj):
        attachments = Attachment.objects.filter(task=obj)
        serializer = GetAttachmentSerializer(attachments, many=True)
        return serializer.data

    class Meta:
        model = Task
        fields = '__all__'
