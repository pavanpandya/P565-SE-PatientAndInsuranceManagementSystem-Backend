from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DoctorSignupSerializer
from .models import OTPVerification, Doctor
from common.utils import send_otp_to_email
from django.contrib.auth import authenticate
from .serializers import DoctorLoginSerializer, DoctorSignupSerializer, DoctorProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from patient.models import PatientAppointment
from django.contrib.sessions.backends.db import SessionStore


class DoctorSignupAPIView(APIView):
    def post(self, request):
        serializer = DoctorSignupSerializer(data=request.data)
        if serializer.is_valid():
            # Save the doctor
            doctor = serializer.save()

            # Generate OTP and send it to the doctor's email
            otp = send_otp_to_email(doctor.email)
            OTPVerification.objects.create(doctor=doctor, otp=otp)

            return Response({
                'message': 'Account created successfully. Please verify your account using the OTP sent to your registered email address.'
            }, status=status.HTTP_201_CREATED)
        
        # Return errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorVerifySignupOTPAPIView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        # Check if the OTP is 6 digits long
        if len(otp) != 6:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Try to find an OTPVerification instance with the provided OTP
        otp_instance = OTPVerification.objects.filter(otp=otp).first()
        
        # If no OTP instance is found or it doesn't match any doctor, return an error
        if not otp_instance:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the doctor associated with the OTP instance
        doctor = otp_instance.doctor
        
        # Mark the doctor as verified
        doctor.is_verified = True
        doctor.save()

        # Delete the OTP verification record
        otp_instance.delete()

        return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)


class DoctorLoginAPIView(APIView):
    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            licence_number = serializer.validated_data.get('licence_number')
            password = serializer.validated_data.get('password')

            # Find doctor using licence_number
            try:
                doctor = Doctor.objects.get(licence_number=licence_number)
            except Doctor.DoesNotExist:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            print(f"Doctor: {doctor.email}")
            print(f"Password: {password}")

            user = authenticate(email='deeppandya1502@gmail.com', password='1234')
            print(f"Authenticated User: {user}")

            # Authenticate the doctor using Django's authenticate method
            authenticated_doctor = authenticate(email=doctor.email, password=password)
            if not authenticated_doctor:
                return Response({'message': 'Authenication Failed'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate an OTP and send it to the doctor's email
            otp = send_otp_to_email(doctor.email)
            OTPVerification.objects.create(doctor=doctor, otp=otp)

            # Respond with a success message
            return Response({'message': 'OTP sent to your registered email address'}, status=status.HTTP_200_OK)

        # Return errors if the data is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DoctorVerifyLoginOTPAPIView(APIView):
    def post(self, request):
        # Extract the OTP from the request data
        otp = request.data.get('otp')

        # Check if the OTP is a 6-digit code
        if len(otp) != 6:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Find the OTPVerification instance using the provided OTP
        otp_instance = OTPVerification.objects.filter(otp=otp).first()
        
        # Handle case where no OTP instance is found or the OTP does not match
        if not otp_instance:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the doctor associated with the OTP instance
        doctor = otp_instance.doctor
        
        # Check if the OTP matches an OTP for the doctor's email and provided OTP
        if not OTPVerification.objects.filter(doctor__email=doctor.email, otp=otp).exists():
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Delete the OTP verification record
        OTPVerification.objects.filter(doctor__email=doctor.email, otp=otp).delete()
        
        # Generate access token and refresh token for the doctor
        refresh = RefreshToken.for_user(doctor)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_200_OK)
    

class DoctorProfileRetrieveAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Retrieve session data from the database
            session_store = SessionStore(session_key=request.session.session_key)

            # Retrieve the decoded session data
            session_data = session_store.load()

            # Retrieve the doctor based on the provided ID
            doctor = Doctor.objects.get(id=session_data['_auth_user_id'])

            # Serialize the doctor's data
            serializer = DoctorProfileSerializer(doctor)

            # Return the serialized data with a success status
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            # Handle invalid ID format error
            return Response({'message': 'Invalid doctor ID format'}, status=status.HTTP_400_BAD_REQUEST)
        except Doctor.DoesNotExist:
            # Handle doctor not found error
            return Response({'message': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)    
        

class DoctorFindingsAPIView(APIView):
    def put(self, request):
        try:
            # Check if the request data contains the required fields i.e appointment_id, doctor_findings, admitted_or_not
            required_fields = ['appointment_id', 'doctor_findings', 'admitted_or_not']
            for field in required_fields:
                if not request.data.get(field):
                    return Response({'message': f'The field {field} is required'}, status=status.HTTP_400_BAD_REQUEST)
                
            pk = request.data.get('appointment_id')
            appointment = get_object_or_404(PatientAppointment, pk=pk)
            appointment.doctor_findings = request.data.get('doctor_findings')
            appointment.admitted_or_not = request.data.get('admitted_or_not')
            appointment.save()
            return Response({'message': 'Doctor findings updated successfully'}, status=status.HTTP_200_OK)
        
        except PatientAppointment.DoesNotExist:
            return Response({'error': 'Patient appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)