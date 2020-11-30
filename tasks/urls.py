from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('sign-up', views.sign_up, name="sign-up"),
    path('sign-in', views.sign_in, name="sign-in"),
    path('log-out', views.log_out, name="log-out"),
    path('update-email', views.update_email, name="update-email"),
    path('<str:list_id>/send-via-email', views.send_list_by_email, name="send-via-email"),
    path('<str:list_id>/download', views.download_file, name="download"),
    path('<str:list_id>/tasks', views.list_tasks, name="tasks"),
    path('<str:list_id>/tasks', views.list_tasks, name="add-task"),
    path('delete-list/<str:list_id>/', views.delete_list, name="delete-list"),
    path('<str:list_id>/tasks/update-task/<str:pk>/', views.update_task, name="update-task"),
    path('<str:list_id>/tasks/delete-task/<str:pk>/', views.delete_task, name="delete-task")
]
