from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Hospital
from .serializers import HospitalCreationSerializer, HospitalSerializer, HospitalUpdateSerializer

class HospitalRegistrationAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = HospitalCreationSerializer(data=request.data)
            if serializer.is_valid():
                hospital = serializer.save()
                return Response(HospitalSerializer(hospital).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the exception (if desired)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HospitalListAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            hospitals = Hospital.objects.all()
            serializer = HospitalSerializer(hospitals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception (if desired)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HospitalUpdateAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def put(self, request, hospital_id):
        try:
            hospital = Hospital.objects.get(id=hospital_id)
        except Hospital.DoesNotExist:
            return Response({'error': 'Hospital not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Log the exception (if desired)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            serializer = HospitalUpdateSerializer(hospital, data=request.data, partial=True)
            if serializer.is_valid():
                hospital = serializer.save()
                return Response(HospitalSerializer(hospital).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the exception (if desired)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
