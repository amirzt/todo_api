from rest_framework import urls

from . import views

urlpatterns = [
    urls.path('login/', views.login, name='login'),
]