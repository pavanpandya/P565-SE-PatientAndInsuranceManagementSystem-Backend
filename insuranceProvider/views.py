
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from models import InsuranceProvider, Patient

@login_required
def insurance_provider(request):
    records = InsuranceProvider.objects.all()
    no_of_packages = len(records)
    revenue_gen = sum(i.revenue for i in records)
    count = sum(i.people_enrolled for i in records)
    return render(request, 'insurance_provider/insurance_providers.html', {'name': 'insuranceProvider', 'packages': records, 'no_of_packages': no_of_packages, 'no_of_patients': count, 'Revenue_gen': revenue_gen})

@login_required
def create_insurance_package(request):
    if request.method == 'POST':
        p_name = request.POST.get('package_name')
        p_description = request.POST.get('package_description')
        i_duration = request.POST.get('insurance_duration')
        pr = request.POST.get('price')
        a = request.POST.get('age')
        InsuranceProvider.objects.create(package_name=p_name, package_description=p_description, insurance_duration=i_duration, age=a, price=pr)
        return redirect('insurance_provider')
    return render(request, 'insurance_provider/create_insurance_packages.html', {'name': 'insuranceProvider'})

@login_required
def suggest_insurance(request, token, insurance_id):
    low, high = map(int, token.split('-'))
    records_suggest = Patient.objects.filter(age__range=(low, high))
    insurance_details = InsuranceProvider.objects.get(id=insurance_id)
    return render(request, 'insurance_provider/suggest_insurance.html', {'current_user': request.user, 'name': 'insuranceProvider', 'suggestedNames': records_suggest, 'insurance_id': insurance_details.id})

@login_required
def suggest_insurance_patient(request, token, insurance_pack):
    update_details = Patient.objects.get(id=token)
    update_details.insurance_package = insurance_pack
    update_details.save()
    return render(request, 'insurance_provider/suggest_insurance_patient.html', {'current_user': request.user, 'name': 'insuranceProvider'})
