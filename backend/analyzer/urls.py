from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze/', views.analyze_video, name='analyze_video'),
    path('dashboard/<str:video_id>/', views.dashboard, name='dashboard'),
]
