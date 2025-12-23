from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DoctorLocationForm
from .models import DoctorLocation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Appointment, DoctorLocation
from .forms import AppointmentForm
from accounts.models import CustomUser
from datetime import datetime, timedelta
from .models import CustomUser, DoctorLocation, Appointment
from datetime import datetime, timedelta, date



def doctor_list(request):
    doctors = CustomUser.objects.filter(role="doctor")
    return render(request, "appointments/doctor_list.html", {"doctors": doctors})


@login_required
def add_location(request):
    if request.user.role != "doctor":
        return redirect("home")

    form = DoctorLocationForm()

    if request.method == "POST":
        form = DoctorLocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.doctor = request.user
            location.save()
            return redirect("doctor_locations")

    return render(request, "appointments/add_location.html", {"form": form})


@login_required
def doctor_locations(request):
    locations = DoctorLocation.objects.filter(doctor=request.user)
    return render(request, "appointments/doctor_locations.html", {"locations": locations})

# appointment 

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, role='doctor')

    # Precompute available slots for each location
    available_slots = []
    for loc in doctor.doctor_locations.all():
        start = loc.start_time
        end = loc.end_time
        slots = []
        current = datetime.combine(datetime.today(), start)
        end_dt = datetime.combine(datetime.today(), end)
        while current + timedelta(minutes=30) <= end_dt:
            slot_start = current.time()
            slot_end = (current + timedelta(minutes=30)).time()

            # Check if already booked
            booked = Appointment.objects.filter(
                doctor=doctor,
                location=loc,
                date=datetime.today().date(),
                start_time__lt=slot_end,
                end_time__gt=slot_start,
                status__in=['pending', 'confirmed']
            ).exists()
            if not booked:
                # value = 24h format for parsing
                value = f"{slot_start.strftime('%H:%M')}-{slot_end.strftime('%H:%M')}"
                # display = friendly AM/PM
                display = f"{slot_start.strftime('%I:%M %p')} - {slot_end.strftime('%I:%M %p')}"
                slots.append({'value': value, 'display': display})
            current += timedelta(minutes=30)
        available_slots.append({'location': loc, 'slots': slots})

    error = None

    if request.method == 'POST':
        location_id = request.POST.get('location_id')
        slot = request.POST.get('slot')
        notes = request.POST.get('notes')

        # Validate slot
        try:
            start_str, end_str = slot.strip().split('-')
            start_time = datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.strptime(end_str, "%H:%M").time()
        except:
            error = "Invalid time slot selected."
            start_time = end_time = None

        location = doctor.doctor_locations.get(id=location_id)

        # Check overlapping
        if start_time and end_time:
            overlapping = Appointment.objects.filter(
                doctor=doctor,
                location=location,
                date=datetime.today().date(),
                start_time__lt=end_time,
                end_time__gt=start_time,
                status__in=['pending', 'confirmed']
            )
            if overlapping.exists():
                error = "This slot is already booked. Please choose another time."
            else:
                # Save appointment
                Appointment.objects.create(
                    patient=request.user,
                    doctor=doctor,
                    location=location,
                    date=datetime.today().date(),
                    start_time=start_time,
                    end_time=end_time,
                    notes=notes
                )
                return redirect('appointments_success')

    return render(request, 'appointments/book_appointment.html', {
        'doctor': doctor,
        'available_slots': available_slots,
        'error': error
    })


@login_required
def appointments_success(request):
    return render(request, 'appointments/success.html')




@login_required
def my_appointments(request):
    appointments = request.user.appointments.order_by('-date', '-start_time')
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})


@login_required
def doctor_my_appointments(request):
    if request.user.role != "doctor":
        return redirect('home')

    appointments = request.user.doctor_appointments.order_by('date', 'start_time')

    if request.method == 'POST':
        appt_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        appointment = Appointment.objects.get(id=appt_id, doctor=request.user)
        if action == "confirm":
            appointment.status = "confirmed"
        elif action == "cancel":
            appointment.status = "cancelled"
        appointment.save()
        return redirect('doctor_my_appointments')

    return render(request, 'appointments/doctor_my_appointments.html', {'appointments': appointments})

