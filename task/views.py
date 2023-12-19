from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task.models import Category, Task, SubTask, Reminder, Attachment
from task.serializers import GetCategorySerializer, AddCategorySerializer, AddTaskSerializer, AddSubTaskSerializer, \
    AddReminderSerializer, AddAttachmentSerializer, GetTaskSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories(request):
    global_categories = Category.objects.filter(is_global=True)
    user_categories = Category.objects.filter(user=request.user)
    categories = global_categories | user_categories

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
def add_task(request):
    serializer = AddTaskSerializer(data=request.data,
                                   context={'data': request.data})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_tasks(request):
    if 'category' in request.data:
        tasks = Task.objects.filter(category=request.data['category'],
                                    user=request.user)
    elif 'date' in request.data:
        tasks = Task.objects.filter(due_date=request.data['date'],
                                    user=request.user)
    else:
        tasks = Task.objects.filter(user=request.user)
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
    if 'note' in request.data:
        task.note = request.data['note']
    if 'category' in request.data:
        task.category = Category.objects.get(id=request.data['category'])

    return Response({'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_sub_task(request):
    serializer = AddSubTaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


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
    date = request.data['date']

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



