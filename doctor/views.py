from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Patient, Booking
from django.db import connection
from common import commonUtility
def index(request):
    return render(request, 'index.html')

@login_required
def doctor(request):
    doctor_id = str(request.user.id)
    query = "SELECT pt.firstname, pt.lastname, b.date, b.start_time, b.end_time, b.patient_id FROM booking b JOIN patient pt ON b.patient_id = pt.id WHERE b.status='OPEN' AND b.doctor_id = %s ORDER BY b.start_time;"
    with connection.cursor() as cursor:
        cursor.execute(query, [doctor_id])
        records = cursor.fetchall()
    return render(request, 'doctor/doctor.html', {'name': request.user.first_name, 'appointments': records})

@login_required
def complete_appointment(request, patientId):
    patient = Patient.objects.filter(id=patientId).first()
    return render(request, 'doctor/completeAppointment.html', {'patient': patient})

@login_required
def mark_as_complete_appointment(request, patientId):
    doctor = User.objects.get(email=request.user.email)
    update_booking = Booking.objects.filter(patient_id=patientId, doctor_id=doctor.id).first()
    update_booking.status = 'COMPLETE'
    update_booking.save()
    query = "SELECT pt.firstname, pt.lastname, b.date, b.start_time, b.end_time, b.patient_id FROM booking b JOIN patient pt ON b.patient_id = pt.id WHERE b.status='OPEN' ORDER BY b.start_time;"
    with connection.cursor() as cursor:
        cursor.execute(query)
        records = cursor.fetchall()
    return render(request, 'doctor/doctor.html', {'name': request.user.first_name, 'appointments': records})
