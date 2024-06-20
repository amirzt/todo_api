from rest_framework import serializers

from task.models import Category, Task, SubTask, Reminder, Attachment, Participation
from user.serializers import CustomUserSerializer


class GetParticipationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Participation
        fields = '__all__'


class GetCategorySerializer(serializers.ModelSerializer):
    participation = serializers.SerializerMethodField('get_pa')
    role = serializers.SerializerMethodField('get_role')

    def get_role(self, ca):
        pa = Participation.objects.filter(category=ca,
                                          user=self.context.get('user'))
        if pa.count() == 0:
            return 'owner'
        else:
            return pa.last().role

    @staticmethod
    def get_pa(self):
        return GetParticipationSerializer(Participation.objects.filter(category=self), many=True).data

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
        if 'start_date' in self.context.get('data'):
            task.start_date = self.context.get('data')['start_date']
        if 'due_date' in self.context.get('data'):
            task.due_date = self.context.get('data')['due_date']
        if 'due_time' in self.context.get('data'):
            task.due_time = self.context.get('data')['due_time']
        if 'note' in self.context.get('data'):
            task.note = self.context.get('data')['note']
        if 'color' in self.context.get('data'):
            task.color = self.context.get('data')['color']
        if 'priority' in self.context.get('data'):
            task.priority = self.context.get('data')['priority']
        if 'repeat' in self.context.get('data'):
            task.repeat = self.context.get('data')['repeat']
        task.save()
        return task


class GetTaskSerializer(serializers.ModelSerializer):
    sub_tasks = serializers.SerializerMethodField('get_sub_tasks')
    reminders = serializers.SerializerMethodField('get_reminders')
    attachments = serializers.SerializerMethodField('get_attachments')
    done_subs = serializers.SerializerMethodField('get_done_subs')

    @staticmethod
    def get_done_subs(obj):
        return SubTask.objects.filter(task=obj, status=True).count()

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


class GetCategoryWithTask(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField('get_tasks')

    participation = serializers.SerializerMethodField('get_pa')
    role = serializers.SerializerMethodField('get_role')

    def get_role(self, ca):
        pa = Participation.objects.filter(category=ca,
                                          user=self.context.get('user'))
        if pa.count() == 0:
            return 'owner'
        else:
            return pa.last().role

    @staticmethod
    def get_pa(self):
        return GetParticipationSerializer(Participation.objects.filter(category=self), many=True).data

    @staticmethod
    def get_tasks(obj):
        tasks = Task.objects.filter(category=obj)
        serializer = GetTaskSerializer(tasks, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = '__all__'


class GetGantTask(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'priority', 'start_date', 'due_date', 'finished_date', 'color', 'created_at', 'status']


class GetGanttCategory(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField('get_tasks')

    def get_tasks(self, object):
        tasks = Task.objects.filter(category=object,
                                    due_date__gte=self.context.get('start_date'),
                                    due_date__lte=self.context.get('end_date'))
        serializer = GetGantTask(tasks, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ['name', 'id', 'tasks']


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['role', 'category']

    def save(self, **kwargs):
        pa = Participation(role=self.validated_data['role'],
                           category=self.validated_data['category'],
                           user=self.context.get('user'))
        pa.save()
        return pa
