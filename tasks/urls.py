from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<str:list_id>/tasks', views.list_tasks, name="tasks"),
    path('<str:list_id>/tasks', views.list_tasks, name="add_task"),
    path('<str:list_id>/tasks/update_task/<str:pk>/', views.update_task, name="update_task"),
    path('<str:list_id>/tasks/delete_task/<str:pk>/', views.delete_task, name="delete_task")
]
