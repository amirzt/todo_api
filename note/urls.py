from rest_framework.urls import path
from . import views

urlpatterns = [
    path('get_notes', views.get_notes),
    path('add_note', views.get_notes),
    path('delete_note', views.get_notes),
    path('update_note', views.get_notes),

]