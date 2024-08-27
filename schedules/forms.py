from django import forms
from .models import Appointment, Time
from datetime import datetime


class AppointmentForm(forms.ModelForm):
    time = forms.ModelChoiceField(
        queryset=Time.objects.all(),
        widget=forms.RadioSelect,
        required=True,
        label="Horários",
    )

    class Meta:
        model = Appointment
        fields = ['day', 'time', 'repeat', ]
        widgets = {
            'day': forms.DateInput(attrs={'type': 'date'},),
            'repeat': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'day' in self.data:
            try:
                day = self.data.get('day')
                if day:
                    day = datetime.strptime(day, '%Y-%m-%d').date()
                    self.fields['time'].queryset = Time.objects.exclude(
                        id__in=Appointment.objects.filter(day=day).values_list('time_id', flat=True)
                    )
            except (ValueError, TypeError):
                pass
        else:
            self.fields['time'].queryset = Time.objects.all()
