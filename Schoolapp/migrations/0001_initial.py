# Generated by Django 3.0.5 on 2023-07-21 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prospective_Candidate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=50)),
                ('date_registered', models.DateTimeField(auto_now=True, null=True)),
                ('user_status', models.CharField(blank=True, choices=[('parent', 'Parent'), ('student', 'Student'), ('teacher', 'Teacher'), ('guardian', 'Guardian')], max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UpcommingEvents',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event_name', models.CharField(max_length=100)),
                ('event_description', models.CharField(max_length=600)),
                ('event_date', models.DateField(blank=True, null=True)),
                ('event_time', models.TimeField(blank=True, null=True)),
                ('date_added', models.DateTimeField(auto_now=True, null=True)),
                ('event_location', models.CharField(max_length=300)),
                ('event_status', models.CharField(blank=True, max_length=300, null=True)),
                ('image_description', models.ImageField(blank=True, null=True, upload_to='Schoolapp/media')),
            ],
            options={
                'db_table': 'upcoming_events',
            },
        ),
    ]
