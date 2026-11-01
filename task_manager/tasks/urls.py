from django.urls import path
from . import views



urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
    path('create-task/', views.create_task_view, name='create-task'),
    path('edit-task/<int:task_id>/', views.edit_task_view, name='edit-task'),
]