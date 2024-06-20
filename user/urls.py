from rest_framework import urls

from . import views

urlpatterns = [
    urls.path('login/', views.login, name='login'),
    urls.path('google_register/', views.google_register, name='google_register'),
    urls.path('add_email/', views.add_email),
    urls.path('update_user/', views.update_user),
    urls.path('search_user/', views.search_user),

]
