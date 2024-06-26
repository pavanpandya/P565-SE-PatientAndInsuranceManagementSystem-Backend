# Generated by Django 5.0.4 on 2024-04-19 04:35

import django.db.models.deletion
import insurance_provider.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceProvider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('company_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=15)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InsurancePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=255)),
                ('plan_description', models.TextField()),
                ('plan_cost', models.DecimalField(decimal_places=2, max_digits=10, validators=[insurance_provider.models.InsurancePlan.validate_plan_cost])),
                ('includes_prescription', models.BooleanField(default=False)),
                ('includes_dental', models.BooleanField(default=False)),
                ('includes_vision', models.BooleanField(default=False)),
                ('insurance_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='insurance_provider.insuranceprovider')),
            ],
        ),
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('insurance_provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='insurance_provider.insuranceprovider')),
            ],
        ),
    ]
