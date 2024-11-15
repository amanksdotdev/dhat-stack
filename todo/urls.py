from django.urls import path

from .views import TodoView, delete_todo, mark_done

urlpatterns = [
    path('', TodoView.as_view(), name='todo'),
    path('delete/<int:id>/', delete_todo, name='delete_todo'),
    path('markdone/<int:id>/', mark_done, name='mark_done'),
]
