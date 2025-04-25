from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', main_view, name='main'),
    path('board/', board_view, name='board'),
    path('post/', post_create_view, name='post_create'),
    path('<int:pk>/', post_detail_view, name='post_detail'),
    path('<int:pk>/delete/', post_delete_view, name='post_delete'),
]