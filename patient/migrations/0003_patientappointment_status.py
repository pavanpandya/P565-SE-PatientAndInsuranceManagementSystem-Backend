# Generated by Django 5.0.4 on 2024-04-20 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_patientappointment_doctor_findings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientappointment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]
