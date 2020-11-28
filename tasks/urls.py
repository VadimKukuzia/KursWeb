from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('sign-up', views.index, name="sign-up"),
    path('<str:list_id>/tasks', views.list_tasks, name="tasks"),
    path('<str:list_id>/tasks', views.list_tasks, name="add-task"),
    path('delete-list/<str:list_id>/', views.delete_list, name="delete-list"),
    path('<str:list_id>/tasks/update-task/<str:pk>/', views.update_task, name="update-task"),
    path('<str:list_id>/tasks/delete-task/<str:pk>/', views.delete_task, name="delete-task")
]
