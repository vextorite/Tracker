from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('issue/<str:pk>', views.issue, name='issue'),
    path('create-project/', views.create_project, name='create-project'),
    path('create-issue/', views.create_issue, name='create-issue'),
    path('update-issue/<str:pk>/', views.update_issue, name='update-issue'),

]