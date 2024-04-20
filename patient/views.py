from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from patient.serializers import *
from common.utils import send_otp_to_email, send_appointment_confirmation_email
from patient.models import OTPVerification, Patient
from doctor.models import Doctor
from doctor.views import DoctorProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.contrib.sessions.backends.db import SessionStore
import json
from datetime import datetime


class PatientSignUpAPIView(APIView):
    def post(self, request):
        serializer = PatientSignUpSerializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save()

            # Generate OTP and send it to the patient's email
            otp = send_otp_to_email(patient.email)
            OTPVerification.objects.create(patient=patient, otp=otp)

            return Response({'message': 'Account created successfully. Please verify your account using the OTP sent to your registered email address.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PatientVerifyOTPView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        if len(otp) != 6:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get Patient's email from the OTPVerification model
            otp_instance = OTPVerification.objects.filter(otp=otp).first()
                
            if not otp_instance:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            if not OTPVerification.objects.filter(patient__email=otp_instance.patient.email, otp=otp).exists():
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Mark the patient as verified
            patient = Patient.objects.get(email=otp_instance.patient.email)
            patient.is_verified = True
            patient.save()
            
            # Delete the OTP verification record
            OTPVerification.objects.filter(patient__email=otp_instance.patient.email, otp=otp).delete()
            
            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
        except OTPVerification.DoesNotExist:
            return Response({'message': 'Please enter the OTP.'}, status=status.HTTP_400_BAD_REQUEST)

    

class PatientLoginAPIView(APIView):
    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate the patient
            patient = authenticate(email=email, password=password)
            if not patient:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate OTP and sent it to the patient's email
            otp = send_otp_to_email(patient.email)
            OTPVerification.objects.create(patient=patient, otp=otp)

            return Response({'message': 'OTP sent to your registered email address'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PatientLoginVerifyOTPView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        if len(otp) != 6:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get Patient's email from the OTPVerification model
            otp_instance = OTPVerification.objects.filter(otp=otp).first()
                
            if not otp_instance:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            if not OTPVerification.objects.filter(patient__email=otp_instance.patient.email, otp=otp).exists():
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Delete the OTP verification record
            OTPVerification.objects.filter(patient__email=otp_instance.patient.email, otp=otp).delete()
            
            # Generate access token and refresh token
            refresh = RefreshToken.for_user(otp_instance.patient)
            login(request, otp_instance.patient, backend='patient.authentication.PatientAuthBackend')
            return Response({
                'access': str(refresh.access_token), 
                'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
        except OTPVerification.DoesNotExist:
            return Response({'message': 'Please enter the OTP.'}, status=status.HTTP_400_BAD_REQUEST)
    

class PatientLogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        

class PatientProfileRetrieveAPIView(APIView):
    def get(self, request):
        try:
            # Retrieve session data from the database
            session_store = SessionStore(session_key=request.session.session_key)

            # Retrieve the decoded session data
            session_data = session_store.load()

            # Get patient by _auth_user_id
            patient = Patient.objects.get(id=session_data['_auth_user_id'])
            serializer = PatientSerializer(patient)

            # Return patient data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            # Handle case where patient is not found
            return Response({'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Generic exception handler
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class PatientProfileUpdateAPIView(APIView):
    def put(self, request):
        try:    
            # Retrieve session data from the database
            session_store = SessionStore(session_key=request.session.session_key)

            # Retrieve the decoded session data
            session_data = session_store.load()

            # Get patient by _auth_user_id
            patient = Patient.objects.get(id=session_data['_auth_user_id'])
            serializer = PatientSerializer(patient, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'message': 'Invalid patient ID format'}, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            return Response({'message': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        

class PatientAppointmentBookingAPIView(APIView):
    def post(self, request):
        # Retrieve patient ID from session
        patient_id = request.session.get('_auth_user_id')

        # Add patient ID to request data
        request.data['patient'] = patient_id
        request.data['status'] = 'confirmed'

        serializer = PatientAppointmentBookingSerializer(data=request.data)
        if serializer.is_valid():
            # Create the appointment
            appointment = serializer.save()

            # Automatically create a placeholder review for the appointment
            placeholder_review = PatientReview.objects.create(
                appointment=appointment,
                patient=appointment.patient,
                doctor=appointment.doctor,
                rating=0,  # Set default rating as None
                review=""  # Set default review as empty string
            )

            # Send confirmation emails to patient and doctor
            send_appointment_confirmation_email(appointment, 'patient')
            send_appointment_confirmation_email(appointment, 'doctor')


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        # Get the appointment to update
        appointment = get_object_or_404(PatientAppointment, pk=pk)

        # Check if the appointment date is in the future
        if appointment.appointment_date < datetime.now().date():
            return Response({"error": "Cannot update past appointments"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = PatientAppointmentBookingSerializer(appointment, data=request.data, partial=True)
        
        if serializer.is_valid():
            # Update the appointment
            appointment = serializer.save()

            # Delete the previous review, if exists
            previous_review = appointment.patientreview_set.first()
            if previous_review:
                previous_review.delete()

            # Create a new placeholder review for the updated appointment
            placeholder_review = PatientReview.objects.create(
                appointment=appointment,
                patient=appointment.patient,
                doctor=appointment.doctor,
                rating=0,  # Set default rating as None
                review=""  # Set default review as empty string
            )

            # Send confirmation emails to patient and doctor for the updated appointment
            send_appointment_confirmation_email(appointment, 'patient', updated=True)
            send_appointment_confirmation_email(appointment, 'doctor', updated=True)

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, pk=None):
        # Update status of appointments that have passed their scheduled time
        self.update_completed_appointments()

        if pk:
            # Get a single appointment
            appointment = get_object_or_404(PatientAppointment, pk=pk)
            serializer = PatientAppointmentBookingSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Get all appointments
            appointments = PatientAppointment.objects.all()
            serializer = PatientAppointmentBookingSerializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def update_completed_appointments(self):
        # Get current date and time
        current_datetime = timezone.now()

        # Query appointments that have passed their scheduled time and status is not "completed"
        appointments_to_update = PatientAppointment.objects.filter(
            appointment_date__lte=current_datetime.date(),
            appointment_time__lte=current_datetime.time(),
            status__in=['pending', 'confirmed']
        )

        # Update status to "completed" for each appointment found
        for appointment in appointments_to_update:
            appointment.status = 'completed'
            appointment.save()
        

class PatientReviewAPIView(APIView):
    def get(self, request):
        reviews = PatientReview.objects.all()
        serializer = PatientReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class DoctorSearchAPIView(APIView):
    def get(self, request):
        try:
            # Get query parameters from request
            search_params = request.query_params
            
            # If no search parameters provided, return all doctors
            if not search_params:
                doctors = Doctor.objects.all()
            else:
                # Initialize queryset with all doctors
                doctors = Doctor.objects.all()
                
                # Filter doctors based on search parameters
                if 'name' in search_params:
                    name_query = search_params['name']
                    doctors = doctors.filter(first_name__icontains=name_query) | doctors.filter(last_name__icontains=name_query)
                
                if 'specialty' in search_params:
                    specialty_query = search_params['specialty']
                    doctors = doctors.filter(specialty__icontains=specialty_query)
                
                if 'supports_covid19' in search_params:
                    supports_covid19_query = search_params['supports_covid19']
                    if supports_covid19_query.lower() == 'true':
                        doctors = doctors.filter(supports_covid19=True)
                    elif supports_covid19_query.lower() == 'false':
                        doctors = doctors.filter(supports_covid19=False)
                    else:
                        return Response({"error": "Invalid value for supports_covid19 parameter"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Serialize the queryset
            serializer = DoctorProfileSerializer(doctors, many=True)
            return Response(serializer.data)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)