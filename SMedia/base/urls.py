from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('issue/', views.room, name='issue'),
]