from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


class Time(models.Model):
    hours = models.CharField(max_length=20)

    def __str__(self):
        return self.hours


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    day = models.DateField()
    time = models.ForeignKey(Time, on_delete=models.PROTECT, related_name='appointment')
    date_created = models.DateTimeField(auto_now_add=True)
    repeat = models.BooleanField(default=False)

    class Meta:
        unique_together = ('day', 'time')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.repeat:
            for c in range(1, 9):
                new_day = self.day + timedelta(weeks=c)
                Appointment.objects.create(
                    user=self.user,
                    day=new_day,
                    time=self.time,
                    repeat=False,
                )

    def __str__(self):
        return f"{self.user.username} | day: {self.day} | time: {self.time}"
