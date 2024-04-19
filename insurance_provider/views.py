from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InsuranceProvider, OTPVerification
from .serializers import InsuranceProviderSignupSerializer, InsuranceProviderLoginSerializer, InsurancePlanSerializer, InsuranceProviderSerializer
from common.utils import send_otp_to_email
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import InsurancePlan, InsuranceProvider


class InsuranceProviderSignupAPIView(APIView):
    def post(self, request):
        serializer = InsuranceProviderSignupSerializer(data=request.data)
        if serializer.is_valid():
            insurance_provider = serializer.save()

            # Generate OTP and send it to the provider's email
            otp = send_otp_to_email(insurance_provider.email)
            OTPVerification.objects.create(insurance_provider=insurance_provider, otp=otp)

            return Response({
                'message': 'Account created successfully. Please verify your account using the OTP sent to your registered email address.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceProviderLoginAPIView(APIView):
    def post(self, request):
        serializer = InsuranceProviderLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate the insurance provider
            insurance_provider = authenticate(email=email, password=password)
            if not insurance_provider:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate OTP and send it to the provider's email
            otp = send_otp_to_email(insurance_provider.email)
            OTPVerification.objects.create(insurance_provider=insurance_provider, otp=otp)

            return Response({'message': 'OTP sent to your registered email address'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InsuranceProviderVerifySignupOTPAPIView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        if len(otp) != 6:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Find the OTPVerification instance using the provided OTP
            otp_instance = OTPVerification.objects.filter(otp=otp).first()
                
            if not otp_instance:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve the insurance provider associated with the OTP
            insurance_provider = otp_instance.insurance_provider
            
            # If the OTP is invalid, return an error response
            if not OTPVerification.objects.filter(insurance_provider__email=insurance_provider.email, otp=otp).exists():
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Verify the insurance_provider
            insurance_provider.is_verified = True
            insurance_provider.save()
            
            # Delete the OTP verification record
            OTPVerification.objects.filter(insurance_provider__email=insurance_provider.email, otp=otp).delete()

            return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
        
        except OTPVerification.DoesNotExist:
            return Response({'message': 'Please enter the OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class InsuranceProviderVerifyLoginOTPAPIView(APIView):
    def post(self, request):
        otp = request.data.get('otp')

        if len(otp) != 6:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Find the OTPVerification instance using the provided OTP
            otp_instance = OTPVerification.objects.filter(otp=otp).first()
                
            if not otp_instance:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Retrieve the insurance provider associated with the OTP
            insurance_provider = otp_instance.insurance_provider
            
            # If the OTP is invalid, return an error response
            if not OTPVerification.objects.filter(insurance_provider__email=insurance_provider.email, otp=otp).exists():
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Delete the OTP verification record
            OTPVerification.objects.filter(insurance_provider__email=insurance_provider.email, otp=otp).delete()

            # Generate access token and refresh token
            refresh = RefreshToken.for_user(insurance_provider)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        
        except OTPVerification.DoesNotExist:
            return Response({'message': 'Please enter the OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        

class InsuranceProviderProfileRetrieveAPIView(APIView):
    # permission_classes = [IsAuthenticated] 

    def get(self, request, provider_id):
        try:
            # Retrieve the insurance provider instance using the ID
            provider = InsuranceProvider.objects.get(id=provider_id)

            # Serialize the insurance provider instance
            serializer = InsuranceProviderSerializer(provider)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            # Handle invalid provider ID format
            return Response({'message': 'Invalid provider ID format'}, status=status.HTTP_400_BAD_REQUEST)

        except InsuranceProvider.DoesNotExist:
            # Handle case when the provider does not exist
            return Response({'message': 'Insurance provider not found'}, status=status.HTTP_404_NOT_FOUND)


class InsuranceProviderPlansAPIView(APIView):
    # permission_classes = [IsAuthenticated] 

    def get(self, request, provider_id):
        try:
            # Get the insurance provider instance
            provider = InsuranceProvider.objects.get(id=provider_id)

            # Get all plans provided by the insurance provider
            plans = InsurancePlan.objects.filter(insurance_provider=provider)

            # Serialize the plans
            serializer = InsurancePlanSerializer(plans, many=True)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            # Handle invalid provider ID format
            return Response({'message': 'Invalid provider ID format'}, status=status.HTTP_400_BAD_REQUEST)

        except InsuranceProvider.DoesNotExist:
            # Handle case when the provider does not exist
            return Response({'message': 'Insurance provider not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, provider_id, plan_id):
        try:
            # Get the insurance provider instance
            provider = InsuranceProvider.objects.get(id=provider_id)

            # Get the specific plan provided by the insurance provider
            plan = InsurancePlan.objects.get(insurance_provider=provider, id=plan_id)

            # Deserialize the request data
            serializer = InsurancePlanSerializer(plan, data=request.data)

            if serializer.is_valid():
                # Save the updated plan details
                serializer.save()
                
                return Response({'message': 'Plan updated successfully', 'plan': serializer.data}, status=status.HTTP_200_OK)
            
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            # Handle invalid plan ID format
            return Response({'message': 'Invalid plan ID format'}, status=status.HTTP_400_BAD_REQUEST)

        except (InsuranceProvider.DoesNotExist, InsurancePlan.DoesNotExist):
            # Handle case when the provider or plan does not exist
            return Response({'message': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def post(self, request, provider_id):
        try:
            # Get the insurance provider instance
            provider = InsuranceProvider.objects.get(id=provider_id)

            # Deserialize the request data
            serializer = InsurancePlanSerializer(data=request.data)

            if serializer.is_valid():
                # Save the new plan details
                serializer.save(insurance_provider=provider)
                
                return Response({'message': 'Plan created successfully', 'plan': serializer.data}, status=status.HTTP_201_CREATED)
            
            # Return validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            # Handle invalid provider ID format
            return Response({'message': 'Invalid provider ID format'}, status=status.HTTP_400_BAD_REQUEST)

        except InsuranceProvider.DoesNotExist:
            # Handle case when the provider does not exist
            return Response({'message': 'Insurance provider not found'}, status=status.HTTP_404_NOT_FOUND)

