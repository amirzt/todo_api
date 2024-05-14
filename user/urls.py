from rest_framework import urls

from . import views

urlpatterns = [
    urls.path('login/', views.login, name='login'),
    urls.path('google_register/', views.google_register, name='google_register'),
]
