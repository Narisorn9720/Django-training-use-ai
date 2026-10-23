from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('todos/create/', views.todo_create, name='todo_create'),
    path('todos/<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('todos/<int:pk>/delete/', views.todo_confirm_delete, name='todo_confirm_delete'),
    path('todos/<int:pk>/complete/', views.todo_complete, name='todo_complete'),
    path('todos/<int:pk>/cancel/', views.todo_cancel, name='todo_cancel'),
]