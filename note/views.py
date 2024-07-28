from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from note.models import Note
from note.serializers import GetNoteSerializer, AddNoteSerializer
from user.models import CustomUser


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_notes(request):
    notes = Note.objects.filter(user_id=request.user.id).order_by('-created_at')
    serializer = GetNoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_note(request):
    serializer = AddNoteSerializer(data=request.data,
                                   context={"user": CustomUser.objects.get(id=request.user.id)})
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_note(request):
    note = Note.objects.get(id=request.data['id'])
    note.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_note(request):
    note = Note.objects.get(id=request.data['id'])
    if 'title' in request.data:
        note.title = request.data['title']
    if 'description' in request.data:
        note.description = request.data['description']
    note.save()
    return Response(status=status.HTTP_200_OK)