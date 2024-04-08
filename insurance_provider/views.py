from rest_framework import generics, status
from rest_framework.response import Response
from .models import InsuranceProvider, InsurancePlan
from .serializers import InsuranceProviderSerializer, InsurancePlanSerializer
from rest_framework.permissions import AllowAny

class InsuranceProviderSignupAPIView(generics.CreateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer

class InsuranceProviderProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer

class InsurancePlanListCreateAPIView(generics.ListCreateAPIView):
    queryset = InsurancePlan.objects.all()
    serializer_class = InsurancePlanSerializer

class InsurancePlanRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InsurancePlan.objects.all()
    serializer_class = InsurancePlanSerializer
