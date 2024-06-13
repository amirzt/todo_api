import datetime
from datetime import timedelta

from datetime import datetime
# from django.utils import timezone

from django.db import models
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task.models import Category, Task, SubTask, Reminder, Attachment, Participation
from task.serializers import GetCategorySerializer, AddCategorySerializer, AddTaskSerializer, \
    AddReminderSerializer, AddAttachmentSerializer, GetTaskSerializer, GetCategoryWithTask, GetGanttCategory, \
    ParticipationSerializer
from user.models import CustomUser


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    # global_categories = Category.objects.filter(is_global=True)
    user_categories = Category.objects.filter(user=request.user)
    participant_categories = Category.objects.filter(participation__user=request.user)

    categories = user_categories | participant_categories
    categories = categories.distinct()
    # categories = user_categories

    serializer = GetCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):
    serializer = AddCategorySerializer(data=request.data,
                                       context={'user': request.user})
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_category(request):
    category = Category.objects.get(id=request.data['id'])
    category.delete()
    return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_category(request):
    category = Category.objects.get(id=request.data['id'])
    category.name = request.data['name']
    category.save()
    return Response(status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_task(request):
    serializer = AddTaskSerializer(data=request.data,
                                   context={'data': request.data,
                                            'user': request.user})
    if serializer.is_valid():
        task = serializer.save()
        if 'sub_tasks' in request.data:
            for sub_task in request.data['sub_tasks']:
                sub = SubTask(title=sub_task,
                              task=task)
                sub.save()
        if 'reminder' in request.data:
            reminder = Reminder(time=request.data['reminder'], task=task)
            reminder.save()
        return Response({"id": task.id})
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    normal_tasks = Task.objects.filter(due_date=request.data['date'],
                                       user=request.user).order_by('-created_at')

    date = timezone.make_aware(datetime.strptime(request.data['date'], "%Y-%m-%d"))

    daily_repeat = Task.objects.filter(repeat='Daily',
                                       user=request.user).order_by('-created_at')

    # print(date.weekday())
    weekly_repeat = Task.objects.filter(due_date__week_day=date.weekday(),
                                        repeat='Weekly',
                                        user=request.user).order_by('-created_at')
    # print(weekly_repeat.last().due_date.weekday())
    monthly_repeat = Task.objects.filter(due_date__day=date.day,
                                         repeat='Monthly',
                                         user=request.user).order_by('-created_at')

    yearly_repeat = Task.objects.filter(due_date__day=date.day,
                                        due_date__month=date.month,
                                        repeat='Yearly',
                                        user=request.user).order_by('-created_at')

    # participant
    participant_tasks = Task.objects.filter(category__participation__user=request.user,
                                            due_date=request.data['date'], )

    tasks = normal_tasks | daily_repeat | weekly_repeat | monthly_repeat | yearly_repeat | participant_tasks

    tasks = tasks.distinct()

    if 'sort' in request.data:
        if request.data['sort'] == 'due_date':
            tasks = tasks.order_by('-due_date')
        if request.data['sort'] == 'created_at':
            tasks = tasks.order_by('created_at')
        if request.data['sort'] == '-created_at':
            tasks = tasks.order_by('-created_at')

    serializer = GetTaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_tasks_by_category(request):
    categories = Category.objects.filter(user=request.user).order_by('-created_at')
    serializer = GetCategoryWithTask(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_favorites(request):
    tasks = Task.objects.filter(user=request.user,
                                is_starred=True).order_by('-created_at')
    serializer = GetTaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_task(request):
    task = Task.objects.get(id=request.data['id'])
    task.delete()
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_task(request):
    task = Task.objects.get(id=request.data['id'])

    if 'title' in request.data:
        task.title = request.data['title']
    if 'due_date' in request.data:
        task.due_date = request.data['due_date']
    if 'due_time' in request.data:
        task.due_time = request.data['due_time']
    if 'is_starred' in request.data:
        task.is_starred = request.data['is_starred']
    if 'status' in request.data:
        task.status = request.data['status']
        if task.status:
            task.finished_date = datetime.now()
    if 'note' in request.data:
        task.note = request.data['note']
    if 'repeat' in request.data:
        task.repeat = request.data['repeat']
    if 'category' in request.data:
        task.category = Category.objects.get(id=request.data['category'])
    if 'reminder' in request.data:
        reminder = Reminder.objects.get(task=task)
        if request.data['reminder'] == 'off':
            reminder.delete()
        else:
            reminder.time = request.data['reminder']
            reminder.save()

    task.save()

    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_sub_task(request):
    task = Task.objects.get(id=request.data['task'])
    subs = request.data['sub_tasks']
    ids = []
    for sub in subs:
        sub_task = SubTask(title=sub['title'], task=task, status=sub['status'])
        sub_task.save()
        ids.append(sub_task.id)
    return Response({'success': True, 'ids': ids}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_sub_task(request):
    sub_task = SubTask.objects.get(id=request.data['id'])
    sub_task.delete()
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_sub_task(request):
    sub_task = SubTask.objects.get(id=request.data['id'])

    if 'title' in request.data:
        sub_task.title = request.data['title']
    if 'status' in request.data:
        sub_task.status = request.data['status']
    sub_task.save()
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_sub_task(request):
    sub_task = SubTask.objects.get(id=request.data['id'])
    sub_task.delete()
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_reminder(request):
    try:
        reminder = Reminder.objects.get(task_id=request.data['task'])
        reminder.time = request.data['time']
        reminder.save()
        return Response({'success': True})
    except Reminder.DoesNotExist:
        serializer = AddReminderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_reminder(request):
    reminder = Reminder.objects.get(id=request.data['id'])
    reminder.delete()
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_reminder(request):
    reminder = Reminder.objects.get(id=request.data['id'])

    if 'time' in request.data:
        reminder.time = request.data['time']
    reminder.save()
    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_attachment(request):
    serializer = AddAttachmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_attachment(request):
    attachment = Attachment.objects.get(id=request.data['id'])
    attachment.delete()
    return Response({'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_completed_data(request):
    completed = Task.objects.filter(status=True, user=request.user).count()
    pending = Task.objects.filter(status=False, user=request.user).count()
    return Response({'completed': completed, 'pending': pending})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_weekly_chart(request):
    date = datetime.strptime(request.data['date'], '%Y-%m-%d').date()

    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    # Query the database to get the task count for each day
    task_counts = Task.objects.filter(
        user=request.user,
        due_date__range=(start_of_week, end_of_week),
        status=True
    ).values('due_date').annotate(count=Count('due_date'))

    # Create a dictionary with day as key and count as value
    task_count_dict = {str(start_of_week + timedelta(days=i)): 0 for i in range(7)}
    for task_count in task_counts:
        task_count_dict[str(task_count['due_date'])] = task_count['count']

    return Response(task_count_dict)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def next_seven_tasks(request):
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=6)

    tasks = Task.objects.filter(
        due_date__range=(start_date, end_date),
        user=request.user
    )
    serializer = GetTaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pending_by_category(request):
    categories_with_counts = Category.objects.filter(user=request.user).annotate(
        uncompleted_tasks_count=Count('task', filter=models.Q(task__user=request.user, task__status=False))
    )

    # Filter out categories with zero uncompleted tasks
    categories_with_counts = categories_with_counts.filter(uncompleted_tasks_count__gt=0)

    # Create a list of tuples containing category name and uncompleted tasks count
    result_list = [(category.name, category.uncompleted_tasks_count) for category in categories_with_counts]

    return Response(result_list)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_task(request):
    search = request.data['search']
    tasks = Task.objects.filter(
        Q(title__icontains=search),
        user=request.user
    )
    serializer = GetTaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_gantt(request):
    categories = Category.objects.filter(user=request.user)
    serializer = GetGanttCategory(
        categories, many=True,
        context={'start_date': request.data['start_date'],
                 'end_date': request.data['end_date']})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_participation(request):
    try:
        user = CustomUser.objects.get(email=request.data['email'])

        serializer = ParticipationSerializer(data=request.data,
                                             context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    except CustomUser.DoesNotExist:
        return Response({"message": "No user found with this email"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_participation(request):
    pa = Participation.objects.get(id=request.data['id'])
    pa.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_participation(request):
    pa = Participation.objects.get(id=request.data['id'])
    pa.role = request.data['role']
    pa.save()
    return Response(status=status.HTTP_200_OK)
