from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from task.models import Category
from user.models import CustomUser


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    package_name = request.data['package_name']

    try:
        if 'email' in request.data:
            user = CustomUser.objects.get(email=request.data['email'],
                                          package_name=package_name)
        else:
            user = CustomUser.objects.get(device_id=request.data['device_id'],
                                          package_name=package_name)
        expired = True if user.expire_date < timezone.now() else False
    except CustomUser.DoesNotExist:

        user = CustomUser(device_id=request.data['device_id'],
                          package_name=package_name)
        user.save()
        expired = True

    user.is_active = True
    user.save()

    # add default categorise
    user_categories = Category.objects.filter(user=user)
    if user_categories.count() == 0:
        global_categories = Category.objects.filter(is_global=True)
        for category in global_categories:
            new_category = Category(name=category.name,
                                    user=user,
                                    is_global=False)
            new_category.save()

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key,
                     'expired': expired,
                     'username': user.username,
                     'expire_date': user.expire_date
                     })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def google_register(request):
    user = CustomUser.objects.get(id=request.user.id)
    user.email = request.data['email']
    user.save()
    return Response({'message': 'Email has been added successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_email(request):
    user = CustomUser.objects.get(id=request.user.id)

    if user.email is not None:
        if user.check_password(request.POST.get('password')):
            return Response({
                'exist': True
            }, status=200)
        else:
            return Response({
                'message': 'رمز ورود اشتباه است'
            }, status=403)
    else:
        user.set_password(request.data['password'])
        user.email = request.data['email']
        user.name = request.data['email'].split('@')[0]
        user.is_active = True
        user.save()

        return Response({
            'exist': False
        }, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = CustomUser.objects.get(id=request.user.id)

    if 'name' in request.data:
        user.name = request.data['name']

    user.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_user(request):
    try:
        user = CustomUser.objects.get(email=request.data['email'])
        return Response({
            'name': user.name
        })
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "not found"})