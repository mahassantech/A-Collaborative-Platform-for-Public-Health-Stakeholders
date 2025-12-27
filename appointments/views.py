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
from datetime import datetime, date as today_date, timedelta
from blog.models import Notification   
from subscriptions.utils import can_book_appointment
from django.contrib import messages
from subscriptions.models import UserSubscription


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

# Helper function
def has_active_premium(user):
    """Check if user has an active premium subscription"""
    try:
        return user.usersubscription.is_premium()
    except UserSubscription.DoesNotExist:
        return False

@login_required
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, role="doctor")
    try:
        subscription = request.user.usersubscription
    except UserSubscription.DoesNotExist:
        messages.error(request, "You need a premium subscription to book an appointment.")
        return redirect("subscription_plans")

    if not subscription.is_premium():
        messages.error(request, "Only premium users can book appointments.")
        return redirect("subscription_plans")

    error = None
    available_slots = []

    # ================= POST REQUEST =================
    if request.method == "POST":
        location_id = request.POST.get("location_id")
        slot_value = request.POST.get("slot")
        date_str = request.POST.get("date")
        notes = request.POST.get("notes")

        if not (location_id and slot_value and date_str):
            error = "Please select date, location and time slot."
        else:
            location = get_object_or_404(
                DoctorLocation, id=location_id, doctor=doctor
            )

            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # 🔴 BLOCK BACK DATE
            if date < today_date.today():
                error = "You cannot book an appointment for a past date."
            else:
                # 🔹 DAY VALIDATION
                weekday = date.strftime("%a")  # Sun, Mon
                allowed_days = [d.strip() for d in location.days.split(",")]

                if weekday not in allowed_days:
                    error = f"Doctor is not available on {weekday}"
                else:
                    start_str, end_str = slot_value.split("-")
                    start_time = datetime.strptime(
                        start_str.strip(), "%H:%M"
                    ).time()
                    end_time = datetime.strptime(
                        end_str.strip(), "%H:%M"
                    ).time()

                    # 🔹 SLOT ALREADY BOOKED?
                    exists = Appointment.objects.filter(
                        doctor=doctor,
                        location=location,
                        date=date,
                        start_time=start_time,
                        status__in=["pending", "confirmed"]
                    ).exists()

                    if exists:
                        error = "This slot is already booked."
                    else:
                        Appointment.objects.create(
                            patient=request.user,
                            doctor=doctor,
                            location=location,
                            date=date,
                            start_time=start_time,
                            end_time=end_time,
                            notes=notes
                        )
                        messages.success(request, "Appointment booked successfully!")
                        return redirect("appointments_success")

    # ================= SLOT GENERATION (GET) =================
    for loc in doctor.doctor_locations.all():
        slots = []
        current = datetime.combine(today_date.today(), loc.start_time)
        end_dt = datetime.combine(today_date.today(), loc.end_time)

        while current + timedelta(minutes=30) <= end_dt:
            s = current.time()
            e = (current + timedelta(minutes=30)).time()
            slots.append({
                "value": f"{s.strftime('%H:%M')}-{e.strftime('%H:%M')}",
                "display": f"{s.strftime('%I:%M %p')} - {e.strftime('%I:%M %p')}"
            })
            current += timedelta(minutes=30)

        available_slots.append({
            "location": loc,
            "slots": slots
        })

    return render(request, "appointments/book_appointment.html", {
        "doctor": doctor,
        "available_slots": available_slots,
        "error": error,
        "today": today_date.today()
    })


@login_required
def appointments_success(request):
    return render(request, 'appointments/success.html')


@login_required
def my_appointments(request):
    # latest appointment first
    appointments = request.user.appointments.order_by('-created_at')
    return render(request, 'appointments/my_appointments.html', {'appointments': appointments})





@login_required
def doctor_my_appointment(request):
    if request.user.role != "doctor":
        return redirect('home')

    appointments = request.user.doctor_appointments.order_by('date', 'start_time')

    if request.method == 'POST':
        appt_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        meeting_link = request.POST.get('meeting_link')  # only for confirm

        appointment = get_object_or_404(
            Appointment,
            id=appt_id,
            doctor=request.user
        )

        patient = appointment.patient
        doctor_name = request.user.username

        # ---------- ACTIONS ----------
        if action == "confirm":
            appointment.status = "confirmed"
            appointment.meeting_link = meeting_link

            Notification.objects.create(
                user=patient,
                message=f"Dr. {doctor_name} confirmed your appointment on {appointment.date}. Meeting link added."
            )

        elif action == "cancel":
            appointment.status = "cancelled"

            Notification.objects.create(
                user=patient,
                message=f"Dr. {doctor_name} cancelled your appointment on {appointment.date}."
            )

        elif action == "complete":
            appointment.status = "completed"

            Notification.objects.create(
                user=patient,
                message=f"Your appointment with Dr. {doctor_name} has been completed."
            )

        appointment.save()
        return redirect('doctor_my_appointment')

    # Separate appointments
    upcoming = appointments.filter(status__in=['pending', 'confirmed'])
    past = appointments.filter(status__in=['completed', 'cancelled'])

    return render(request, 'appointments/doctor_appointments.html', {
        'upcoming': upcoming,
        'past': past
    })