from django.urls import path
from . import views

urlpatterns = [
    path('resetPassword/', views.reset_password, name='reset_password'),
    path('google/', views.google, name='google'),
    path('authorize/', views.authorize, name='authorize'),
]
