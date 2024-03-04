
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from authlib.integrations.requests_client import OAuth2Session

def reset_password(request):
    if request.method == 'GET':
        return render(request, 'reset_password.html')
    elif request.method == 'POST':
        send_mail(
            'Reset Password - Carebox',
            'Reset password link',
            settings.DEFAULT_FROM_EMAIL,
            ['amitaranade43@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'reset_mail_sent.html')

def google(request):
    client_id = '1091902576282-ckdfagtps3648hmrm2u2tgnv2fhrvial.apps.googleusercontent.com'
    client_secret = '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'
    redirect_uri = request.build_absolute_uri(reverse('authorize'))

    google = OAuth2Session(client_id, client_secret, redirect_uri=redirect_uri, scope='openid email profile')

    authorization_url, state = google.create_authorization_url('https://accounts.google.com/.well-known/openid-configuration')

    return redirect(authorization_url)

@login_required
def authorize(request):
    # Handle authorization and access token retrieval from Google
    return render(request, 'patient.html')

def get_query(search_query, disease, covid_care, location):
    query = "select distinct u.first_name, u.last_name, doc.fees, h.location, (case when doc.rating is null then 0 else doc.rating end) as rating, doc.profile_pic from doctor_disease dd natural join doctor doc natural join public.user u, hospital h "        
    query_condition = "where 1 = 1 and doc.hospital_id = h.id "
    
    if len(search_query) > 0:
        query_condition += f" and UPPER(u.first_name) like UPPER('{search_query}')"
    if disease != 'select':
        query_condition += f" and dd.doctor_id = doc.id and dd.disease_id = (select d.id from disease d where d.name = '{disease}')"
    covid_care_bool_val = False
    if covid_care != 'select':
        if covid_care == 'YES':
            covid_care_bool_val = True
        query_condition += f" and doc.provide_covid_care = {covid_care_bool_val}"
    if location != 'select':
        query_condition += f" and h.location = '{location}'"
    
    query += query_condition + " ;"
    print("Formulated query is:", query)
    
    return query
