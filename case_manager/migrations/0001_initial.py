# Generated by Django 5.1.4 on 2025-03-19 19:05

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
            name='MentorshipSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('self_discovery', 'Self-Discovery'), ('career', 'Career'), ('behavioral_change', 'Behavioral Change')], max_length=50)),
                ('date', models.DateTimeField()),
                ('notes', models.TextField(blank=True)),
                ('case_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentee_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PerformanceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('progress_summary', models.TextField()),
                ('transformation_outcome', models.CharField(blank=True, choices=[('internship', 'Internship'), ('back_to_school', 'Back to School'), ('business_startup', 'Business Startup')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_reports', to=settings.AUTH_USER_MODEL)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentee_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
