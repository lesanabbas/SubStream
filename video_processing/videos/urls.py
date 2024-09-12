from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('', views.video_list, name='video_list'),
    path('play/<int:pk>/', views.play_video, name='play_video'),
    path('delete/<int:pk>/', views.delete_video, name='delete_video'),

]