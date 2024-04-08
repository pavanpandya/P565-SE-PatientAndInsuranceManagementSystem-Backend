from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, WorkingHour
from .serializers import DoctorSerializer, WorkingHourSerializer
from rest_framework.permissions import AllowAny

class DoctorSignupAPIView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = []

class DoctorProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.first_name

class DoctorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class WorkingHourListCreateAPIView(generics.ListCreateAPIView):
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer

    def perform_create(self, serializer):
        doctor_id = self.request.data.get('doctor')
        doctor = Doctor.objects.get(id=doctor_id)
        serializer.save(doctor=doctor)

class WorkingHourRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer


class DoctorAvailabilityListAPIView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]  # Allow any user to access doctor availability information

    def get_queryset(self):
        # Override get_queryset to prefetch related data for optimization
        return Doctor.objects.prefetch_related('working_hours', 'hospitals')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serialized_data = self.get_serializer(queryset, many=True).data

        # Customize serialized data to include hospital information
        for data in serialized_data:
            # Include hospital names associated with the doctor
            hospitals = [hospital.name for hospital in data['hospitals']]
            data['hospitals'] = hospitals

            # Include working hours along with day, start time, and end time
            working_hours = []
            for working_hour in data['working_hours']:
                working_hours.append({
                    'day_of_week': working_hour['day_of_week'],
                    'start_time': working_hour['start_time'],
                    'end_time': working_hour['end_time']
                })
            data['working_hours'] = working_hours

        return Response(serialized_data)