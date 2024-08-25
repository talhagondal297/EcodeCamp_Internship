from django.urls import path
from .views import task_list, add_task, remove_task, delete_all_tasks

urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('remove/<int:task_id>/', remove_task, name='remove_task'),
    path('delete-all-tasks/', delete_all_tasks, name='delete_all_tasks'),
]
