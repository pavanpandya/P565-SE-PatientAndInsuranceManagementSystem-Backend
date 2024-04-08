from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Patient, PatientHistory, PatientAppointment
from .serializers import PatientSerializer, PatientProfileSerializer, PatientAppointmentSerializer, PatientLoginSerializer, DoctorSearchSerializer
from doctor.models import Doctor
from django.db.models import Q
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from .serializers import VerifyOTPSerializer
from common.utils import generate_otp, send_otp_via_email, send_appointment_confirmation_email
from django.contrib.auth.hashers import check_password
from django.http import Http404



User = get_user_model()

def authenticate_with_email(email=None, password=None):
    try:
        patient = Patient.objects.get(email=email)
        if check_password(password, patient.password):
            return patient
        else:
            return None
    except Patient.DoesNotExist:
        return None

class PatientSignupAPIView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = []

class PatientLoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PatientLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate_with_email(email=email, password=password)
            if user is not None:
                patient = Patient.objects.get(email=email)
                print("User authenticated:", user.email)
                if patient.is_verified:
                    # login(request, user)
                    request.session['email'] = email
                    print("User logged in successfully.")
                    return Response({'detail': 'Logged in successfully.'}, status=status.HTTP_200_OK)
                else:
                    otp = generate_otp()
                    send_otp_via_email(email, otp)
                    request.session['otp'] = otp 
                    request.session['email'] = email
                    print("Email stored in session:", request.session.get('email'))
                    return Response({'detail': 'Account not verified. OTP sent to your email.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                print("Failed login attempt for email:", email)
                return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientVerifyOTPAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['otp']
            email = request.session.get('email')  # Retrieve email from session
            stored_otp = request.session.get('otp')  # Retrieve OTP from session
            if stored_otp != otp:
                return Response({'detail': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Once OTP is verified, remove it and email from session
                del request.session['otp']
                del request.session['email']
                patient = Patient.objects.get(email=email)
                patient.is_verified = True
                patient.save()
                return Response({'detail': 'Account verified successfully.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientProfileAPIView(generics.RetrieveAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = []

    def get_object(self):
        # Retrieve email from session
        email = self.request.session.get('email')
        if email:
            try:
                # Retrieve patient object using the email
                patient = Patient.objects.get(email=email)
                return patient
            except Patient.DoesNotExist:
                raise Http404("Patient does not exist")
        else:
            raise Http404("Email not found in session")


class DoctorSearchAPIView(generics.ListAPIView):
    serializer_class = DoctorSearchSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return Doctor.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(speciality__icontains=query) | Q(department__icontains=query))
        else:
            return Doctor.objects.all()

class PatientAppointmentCreateAPIView(generics.CreateAPIView):
    queryset = PatientAppointment.objects.all()
    serializer_class = PatientAppointmentSerializer
    permission_classes = []

    def perform_create(self, serializer):
        appointment_instance = serializer.save()
        send_appointment_confirmation_email(appointment_instance)
