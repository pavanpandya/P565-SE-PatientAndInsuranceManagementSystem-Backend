import random
from django.core.mail import send_mail
from django.conf import settings

def send_otp_via_email(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for account verification is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def generate_otp():
    # Generate a 6-digit OTP
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_appointment_confirmation_email(appointment):
    subject_patient = 'Appointment Confirmation'
    subject_doctor = 'New Appointment'
    
    message_patient = f'Your appointment with Dr. {appointment.assigned_doctor.first_name} {appointment.assigned_doctor.last_name} on {appointment.appointment_date} at {appointment.appointment_time} has been confirmed.'
    message_doctor = f'You have a new appointment with {appointment.patient.first_name} {appointment.patient.last_name} on {appointment.appointment_date} at {appointment.appointment_time}.'
    
    from_email = settings.EMAIL_HOST_USER
    
    # Send confirmation email to patient
    send_mail(subject_patient, message_patient, from_email, [appointment.patient.email])

    # Send notification email to doctor
    send_mail(subject_doctor, message_doctor, from_email, [appointment.assigned_doctor.email])