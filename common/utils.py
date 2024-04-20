import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_otp_to_email(email):
    otp = generate_otp()
    # print(f'Generated OTP: {otp}')
    subject = 'OTP Verification'
    message = f'Your OTP for account verification is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
    return otp


def generate_otp():
    # Generate a 6-digit OTP
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_appointment_confirmation_email(appointment, recipient_type, updated=False):
    """
    Sends appointment confirmation email to the patient or doctor.
    
    Parameters:
        - appointment: PatientAppointment object
        - recipient_type: 'patient' or 'doctor'
        - updated: Boolean indicating if the appointment is updated
    """
    # Determine recipient email address based on recipient_type
    if recipient_type == "patient":
        recipient_email = appointment.patient.email
    elif recipient_type == "doctor":
        recipient_email = appointment.doctor.email
    else:
        raise ValueError("Invalid recipient type")

    # Prepare context data for the email template
    context = {
        "appointment_date": appointment.appointment_date,
        "appointment_time": appointment.appointment_time,
        "doctor_name": f"{appointment.doctor.first_name} {appointment.doctor.last_name}",  # Assuming doctor has a full_name field
        "patient_name": f"{appointment.patient.first_name} {appointment.patient.last_name}",  # Assuming patient has a full_name field
        "symptoms": appointment.symptoms,
        "reason": appointment.reason,
        "hospital_address": appointment.hospital_address,
        "updated": updated,
    }

    # Choose the appropriate email template
    if recipient_type == "patient":
        template = "appointment_confirmation_patient_email.html"
    else:
        template = "appointment_confirmation_doctor_email.html"

    # Render the email template
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    # Set the subject line
    subject = "Appointment Confirmation"
    if updated:
        subject += " (updated)"

    # Send the email
    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [recipient_email],
        html_message=html_message
    )