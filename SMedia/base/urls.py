from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('issue/<str:pk>', views.issue, name='issue'),
    path('create-issue/', views.create_issue, name='create-issue'),
]