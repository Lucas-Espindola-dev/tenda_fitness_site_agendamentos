from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view, logout_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('schedules.urls')),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    # path('user/<str:username>/'),
    path('logout/', logout_view, name='logout'),
]
