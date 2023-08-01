from django.db import models
from users.models import CustomUser, Student, Staff
from django.db.models.signals import post_save
from django.dispatch import receiver
# import TIME_ZONE
# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=50)
    admin = models.ForeignKey(Staff, on_delete =models.DO_NOTHING)
    members = models.ManyToManyField(Student, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
class Messages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=10000, blank=True, null=True)
    message_file = models.FileField(upload_to='message_files', blank=True, null=True)
    message_image = models.FileField(upload_to='message_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.room.name
class Personal_chat(models.Model):
    name = models.CharField(max_length=50)
    initiator = models.ForeignKey(CustomUser, on_delete =models.DO_NOTHING, related_name='initator')
    recepient = models.ForeignKey(CustomUser, blank=True, on_delete =models.DO_NOTHING, related_name='recipient')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Personal_messages(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,  related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,  related_name='receiver')
    message = models.CharField(max_length=10000, blank=True, null=True)
    message_file = models.FileField(upload_to='message_files', blank=True, null=True)
    message_image = models.FileField(upload_to='message_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.room.name





# @receiver(post_save, sender=Student)
# def add_students_to_chatroom(sender, instance, created, **kwargs):
#     if created:
#         get_class = StudentClass.objects.get()
#         student= Student.objects.filter(student_class=)
        
#         chatroom = Room.objects.filter(admin=student.student_class.staff_id).first()
#         if chatroom:
#             if not instance.student_class:
#                 chatroom.members.remove(instance)
#             else:
#                 chatroom.members.add(*student)
