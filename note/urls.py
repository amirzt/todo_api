from rest_framework.urls import path
from . import views

urlpatterns = [
    path('get_notes/', views.get_notes),
    path('add_note/', views.add_note),
    path('delete_note/', views.delete_note),
    path('update_note/', views.update_note),

]