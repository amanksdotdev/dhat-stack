from django.urls import path

from .views import TodoView, delete_todo

urlpatterns = [
    path('', TodoView.as_view(), name='todo'),
    path('<int:id>/', delete_todo, name='delete_todo'),
]