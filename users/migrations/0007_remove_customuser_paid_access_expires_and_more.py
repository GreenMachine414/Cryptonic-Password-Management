# Generated by Django 5.1.3 on 2024-12-07 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_otpcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='paid_access_expires',
        ),
        migrations.RemoveField(
            model_name='password',
            name='last_used',
        ),
        migrations.RemoveField(
            model_name='password',
            name='username',
        ),
    ]
