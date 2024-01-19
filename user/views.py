from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from task.models import Category
from user.models import CustomUser


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    package_name = request.data['package_name']

    try:
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
