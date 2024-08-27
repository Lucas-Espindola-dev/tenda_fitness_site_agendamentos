from django.contrib import admin
from .models import Appointment, Time


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'day', 'time',)


admin.site.register(Appointment, AppointmentAdmin)


class TimeAdmin(admin.ModelAdmin):
    list_display = ('id', 'hours',)


admin.site.register(Time, TimeAdmin)
