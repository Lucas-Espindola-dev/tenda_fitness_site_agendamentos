from django.urls import path
from schedules import views


urlpatterns = [
    path('', views.home, name='home'),
    path('appointments/', views.AppointmentListView.as_view(), name='appointments-list'),
    path('appointments/new/', views.AppointmentCreateView.as_view(), name='appointments-create'),
    path('users/<str:username>/appointments/', views.UserAppointmentsListView.as_view(), name='user-appointments-list'),
    path('appointments/sucess/', views.sucess_message, name='sucess'),
    path('appointments/<int:pk>/update/', views.AppointmentUpdateView.as_view(), name='appointment-update'),
    path('appointments/<int:pk>/delete/', views.AppointmentDeleteView.as_view(), name='appointment-delete'),
    path('get_available_times/', views.get_available_times, name='get_available_times'),
]
