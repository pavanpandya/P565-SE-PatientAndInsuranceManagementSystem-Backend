from rest_framework.views import APIView
from .serializers import InsuranceCompanyRegistrationSerializer, InsuranceCompanyProfileSerializer, PatientHistorySerializerInsuranceCompanyView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from insurance_provider.models import InsuranceCompany


class IsInsuranceCompany(BasePermission):
    """Custom Permission class for Insurance Company"""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='InsuranceCompany').exists()
    

class CustomAuthToken(APIView):
    """This class returns custom Authentication token for Insurance Company"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        account_approval = user.groups.filter(name='doctor').exists()
        if user.status==False:
            return Response(
                {
                    'message': "Your account is not approved by admin yet!"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        elif account_approval==False:
            return Response(
                {
                    'message': "You are not authorised to login as a doctor"
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            },status=status.HTTP_200_OK)
        

class registrationView(APIView):
    """API endpoint for Insurance Company Registration"""
    permission_classes = []
    
    def post(self, request, format=None):
        registrationSerializer = InsuranceCompanyRegistrationSerializer(data=request.data.get('user_data'))
        profileSerializer = InsuranceCompanyProfileSerializer(data=request.data.get('profile_data'))
        checkregistration = registrationSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkregistration and checkprofile:
            insuranceCompany = registrationSerializer.save()
            profileSerializer.save(user=insuranceCompany)
            return Response({
                'user_data': registrationSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'user_data': registrationSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class insuranceCompanyProfileView(APIView):
    """API endpoint for Insurance Company Profile"""
    permission_classes = [IsInsuranceCompany]
    
    def get(self, request, format=None):
        user = request.user
        profile = InsuranceCompany.objects.get(user=user).get()
        userSerializer = InsuranceCompanyRegistrationSerializer(user)
        profileSerializer = InsuranceCompanyProfileSerializer(profile)
        return Response({
            'user_data': userSerializer.data,
            'profile_data': profileSerializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, format=None):
        user = request.user
        profile = InsuranceCompany.objects.get(user=user).get()
        userSerializer = InsuranceCompanyRegistrationSerializer(user, data=request.data.get('user_data'))
        profileSerializer = InsuranceCompanyProfileSerializer(profile, data=request.data.get('profile_data'))
        checkuser = userSerializer.is_valid()
        checkprofile = profileSerializer.is_valid()
        if checkuser and checkprofile:
            userSerializer.save()
            profileSerializer.save()
            return Response({
                'user_data': userSerializer.data,
                'profile_data': profileSerializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'user_data': userSerializer.errors,
                'profile_data': profileSerializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

class patientHistoryView(APIView):
    """API endpoint for Insurance Company to view patient history"""
    permission_classes = [IsInsuranceCompany]
    
    def get(self, request, uuid, format=None):
        try:
            patient = PatientHistory.objects.get(uuid=uuid)
            serializer = PatientHistorySerializerInsuranceCompanyView(patient)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PatientHistory.DoesNotExist:
            return Response(
                {
                    'message': "Patient History not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )