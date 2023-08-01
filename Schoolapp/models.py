from django.db import models
from users.models import *
import datetime

# Create your models here.
class UpcommingEvents(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=100, null=False)
    event_description = models.CharField(max_length=600, null=False)
    event_date = models.DateField(blank=True, null=True)
    event_time = models.TimeField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now=True, blank=True, null=True)
    event_location = models.CharField(max_length=300, null=False)
    event_status = models.CharField(max_length=300, blank=True, null=True)
    image_description = models.ImageField(upload_to='Schoolapp/media', null=True, blank=True)
    
    class Meta:
        db_table = "upcoming_events"
    def __str__(self):
        return self.event_name
    
    def Time_regulator(self):
        events = UpcommingEvents.objects.all()
        for event in events:
            if event.event_date > datetime.datetime.date.now():
                event.event_status = "Upcomming Event"
                event.event_status.save()
            elif event.event_date < datetime.datetime.date.now():
                event.event_status = "Concluded Event"
                event.event_status.save()

            elif event.event_date == datetime.datetime.date.now():
                event.event_status = "Ongoing Event"
                event.event_status.save()

            else:
                event.event_status = "None"
                event.event_status.save()


class Prospective_Candidate(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(CustomUser, null=True, blank=True,  on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=500)
    email = models.EmailField(max_length=254)
    phone_number=models.CharField(max_length=50)
    date_registered = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = [
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('guardian', 'Guardian'),
    ]
    user_status = models.CharField(choices= status, max_length=50, blank=True, null=True)
    
    def __str__(self):
        return 'Prospectice candidate '+' -- '+self.name
# class Prospective_Candidates(models.Model):
#     id = models.AutoField(primary_key=True)
#     admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     gender_type = [
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#     ]
#     gender = models.CharField(max_length=7, choices=gender_type, default='None')
#     address = models.TextField(null=True, blank=True)
#     department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
#     profile_pic = models.ImageField(upload_to='save_image',null=True, blank=True)
#     session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.DO_NOTHING, null=True)
#     student_class = models.ForeignKey(StudentClass, on_delete=models.DO_NOTHING, null=True)
#     user_types = models.CharField(null=True, blank=True, max_length=10)
#     objects = models.Manager()
#     date_of_birth = models.DateField(null=True, blank=True)
#     parents_phone_number = models.CharField(max_length=15, null=True, blank=True)
#     age = models.IntegerField(blank=True, null=True)
#     parent_name = models.CharField(max_length=500, null=True, blank=True)
#     parentstatus = [
#         ('father', 'Father'),
#         ('mother', 'Mother'),
#         ('guardian', 'Guardian'),
#     ]
#     parent_status = models.CharField(max_length=50, choices=parentstatus, null=True, blank=True)
#     # year_joined = models.DateField(auto_now=False)

#     def __str__(self):
#         return self.admin.username