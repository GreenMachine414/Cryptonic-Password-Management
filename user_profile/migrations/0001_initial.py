# Generated by Django 5.1 on 2024-10-30 19:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(0, 'None'), (1, 'Female'), (2, 'Male'), (3, 'Other')], default=0)),
                ('age', models.IntegerField(default=21)),
                ('picture', models.ImageField(blank=True, upload_to='profile_pictures/')),
                ('custom_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
