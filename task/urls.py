from rest_framework.urls import path

from task import views

urlpatterns = [
    path('get_categories/', views.get_categories),
    path('add_category/', views.add_category),
    path('add_task/', views.add_task),
    path('get_tasks/', views.get_tasks),
    path('get_favorites/', views.get_favorites),
    path('delete_task/', views.delete_task),
    path('add_sub_task/', views.add_sub_task),
    path('add_reminder/', views.add_reminder),
    path('delete_sub_task/', views.delete_sub_task),
    path('update_sub_task/', views.update_sub_task),
    path('delete_reminder/', views.delete_reminder),
    path('update_task/', views.update_task),
    path('update_reminder/', views.update_reminder),
    path('add_attachment/', views.add_attachment),
    path('delete_attachment/', views.delete_attachment),
    path('get_compeleted_data/', views.get_completed_data),
    path('get_weekly_chart/', views.get_weekly_chart),
    path('next_seven_tasks/', views.next_seven_tasks),
    path('pending_by_category/', views.pending_by_category),
    path('delete_category/', views.delete_category),
    path('update_category/', views.update_category),
    path('search_task/', views.search_task),

]