from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from schedules.models import Appointment, Time
from .forms import AppointmentForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin


def home(request):
    return render(request, 'schedules/home.html')


def sucess_message(request):
    return render(request, 'schedules/sucess.html')


class AppointmentListView(UserPassesTestMixin, ListView):
    model = Appointment
    template_name = 'schedules/appointments_list.html'
    context_object_name = 'appointments'

    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        today = timezone.localdate()
        return Appointment.objects.filter(day=today)


@method_decorator(login_required(login_url='login'), name='dispatch')
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'schedules/new_appointment.html'
    success_url = reverse_lazy('sucess')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.method == 'GET' and 'day' in self.request.GET:
            form.fields['time'].queryset = Time.objects.exclude(
                id__in=Appointment.objects.filter(day=self.request.GET['day']).values_list('time_id', flat=True)
            )
        return form

    def form_valid(self, form):
        print("Form is valid. Data:", form.cleaned_data)
        form.instance.user = self.request.user
        response = super().form_valid(form)
        print("Appointment instance:", form.instance)
        return response

    def form_invalid(self, form):
        # Debug: Displaying form errors
        print("Dados submetidos:", self.request.POST)
        print("Erros no formulário:", form.errors)
        return super().form_invalid(form)


@method_decorator(login_required(login_url='login'), name='dispatch')
class UserAppointmentsListView(ListView):
    model = Appointment
    template_name = 'schedules/user_appointments_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        user = User.objects.get(username=self.kwargs['username'])
        now = timezone.now()
        return Appointment.objects.filter(user=user, day__gte=now).order_by('day', 'time')


class AppointmentUpdateView(UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'schedules/appointment_update.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        if self.request.method == 'GET' and 'day' in self.request.GET:
            form.fields['time'].queryset = Time.objects.exclude(
                id__in=Appointment.objects.filter(day=self.request.GET['day']).values_list('time_id', flat=True)
            )
        return form

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('user-appointments-list', kwargs={'username': username})


@method_decorator(login_required(login_url='login'), name='dispatch')
class AppointmentDeleteView(DeleteView):
    model = Appointment
    template_name = 'schedules/appointment_delete.html'

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('user-appointments-list', kwargs={'username': username})


def get_available_times(request):
    selected_date = request.GET.get('date')
    booked_times = Appointment.objects.filter(day=selected_date).values_list('time', flat=True)
    available_times = Time.objects.exclude(id__in=booked_times)

    data = {
        'available_times': [{'id': time.id, 'time': str(time)} for time in available_times]
    }
    return JsonResponse(data)
