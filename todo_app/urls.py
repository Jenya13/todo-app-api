"""
URL mapping for Todo application API. 
"""

from django.urls import path
from todo_app.views import (TodoListAPIView, TodoDetailAPIView,
                            CreateUserAPIView, LogoutUserAPIView, CreateTokenView)

urlpatterns = [
    path('account/register/', CreateUserAPIView.as_view(), name='register'),
    path('account/login/', CreateTokenView.as_view(), name='login'),
    path('account/logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('todos/', TodoListAPIView.as_view(), name='todo-list'),
    path('todos/<int:pk>/', TodoDetailAPIView.as_view(), name='todo-detail')
]
