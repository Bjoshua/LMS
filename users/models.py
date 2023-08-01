from django.db import models
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Permission, Group, User

# Create your models here.

class CustomUser(AbstractUser):
    # user_type_data = [(1, "HOD"),(2, "Staff"),(3, "Student")]
    user_type = models.CharField(default="1", null=True, blank=True, max_length=10)
    user_permissions = models.ManyToManyField(Permission)
    groups = models.ManyToManyField(Group)
    # def __str__(self):
    #     return self.user_type
class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()  
    def __str__(self):
        return self.name
    
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.name
    
    
class StudentClass(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=6, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    objects = models.Manager()
    def __str__(self):
        return self.name


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    staff_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    objects = models.Manager()
    subj_class = models.ForeignKey(StudentClass, on_delete=models.DO_NOTHING, blank=True, null=True)
    def __str__(self):
        return self.name

    
class AdminHOD(models.Model):
    user_type = models.CharField(null=True, blank=True, max_length=10)
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to='admin_image',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.admin.username


def save_image(instance, filename):
    upload_to = 'Images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = 'User_Profile_Pictures/{}.{}'.format(instance.pk, ext)
    return os.path.join(upload_to, filename)

        
class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField(default="None", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(null=True, blank=True, max_length=10)
    form_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, blank=True, null=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()    
    gender_type = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=7, choices=gender_type, default='None', null=True, blank=True)

    profile_pic = models.ImageField(upload_to='save_image',null=True, blank=True)
    def __str__(self):
        return self.admin.username    

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender_type = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=7, choices=gender_type, default='None')
    address = models.TextField(null=True, blank=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='save_image',null=True, blank=True)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE, blank=True, null=True)
    student_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, blank=True, null=True)
    user_types = models.CharField(null=True, blank=True, max_length=10)
    objects = models.Manager()
    date_of_birth = models.DateField(null=True, blank=True)
    parents_phone_number = models.CharField(max_length=15, null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    parent_name = models.CharField(max_length=500, null=True, blank=True)
    parentstatus = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ]
    parent_status = models.CharField(max_length=50, choices=parentstatus, null=True, blank=True)
    # year_joined = models.DateField(auto_now=False)
    subjects = models.ManyToManyField(Subjects)
    def __str__(self):
        return self.admin.username
     
class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_1st_test_marks = models.FloatField( null=True, blank=True)
    subject_2nd_test_marks = models.FloatField(null=True, blank=True)
    subject_assignment_marks = models.FloatField( null=True, blank=True)
    subject_project_marks = models.FloatField( null=True, blank=True)
    subject_exam_marks = models.FloatField( null=True, blank=True)
    subject_total_marks = models.FloatField( null=True, blank=True)
    session = models.ForeignKey(SessionYearModel, on_delete=models.DO_NOTHING)
    grade = models.CharField(max_length=12, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.student_id.admin.first_name + "'s Result"

class StudentLeave(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.student_id.admin.first_name

class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.student_id.admin.first_name

class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.staff_id.admin.first_name  
     
class StaffLeave(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    def __str__(self):
        return self.staff_id.admin.first_name

class Assessment(models.Model):
    name = models.CharField(max_length=100)
    total_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
class CreateAssessment(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    classs = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)
    assessment_text = models.TextField(blank=True, null=True)
    assesment_file = models.FileField(upload_to='media/files/assignment_files', max_length=150, blank=True, null=True)
    use_as_result = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    question_text = models.TextField(blank=True, null=True)
    question_file = models.FileField(upload_to='media/files/assignment_files', max_length=150, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    form_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)
    use_as_assessment = models.BooleanField(null=True, blank=True)
    def __str__(self) -> str:
        return self.subject.name+" "+'Assignment by' + " " +self.created_by.admin.username
    
class Test(models.Model):    
    test = [    
        ('1st', 'First CA Test'),    
        ('2nd', 'Second CA Test'),
        ('3rd', 'Third CA Test'),    
    ]
    id = models.AutoField(primary_key=True)
    form_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)
    test_name = models.CharField(choices = test, max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    test_text = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Staff, on_delete=models.CASCADE, blank=True, null=True)
    test_file = models.FileField(upload_to='media/files/test_files', max_length=150, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.subject.name+" "+'Test by' + " " +self.created_by.admin.username

    
class Examination(models.Model):
    id = models.AutoField(primary_key=True)
    form_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    examination_text = models.TextField(blank=True, null=True)
    examination_file = models.FileField(upload_to='media/files/examination_files', max_length=150, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    
    def __str__(self) -> str:
        return self.subject.name+" "+'Examination by' + " " +self.created_by.admin.username
class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    heading = models.CharField(max_length=150, null=True, blank=True)
    created_by = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    lecture_text = models.TextField(blank=True, null=True)
    lecture_video = models.FileField(upload_to='media/files/Lectures/Videos', max_length=150, blank=True, null=True)
    form_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True)
    lecture_ppt = models.FileField(upload_to='media/files/Lectures/PPT', max_length=150, blank=True, null=True)
    lecture_file = models.FileField(upload_to='media/files/Lectures/File', max_length=150, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    # department
    
    def __str__(self) -> str:
        return self.subject.name+" "+'Lecture by' + " " +self.created_by.admin.username
    
    
class Submitted_Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    submitted_assignment_text = models.TextField(blank=True, null=True)
    submitted_status = models.BooleanField(null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=True, null=True)
    submitted_assignment_file = models.FileField(upload_to='media/files/submitted_assignment_files', max_length=150, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    submitted_by = models.ForeignKey(Student, related_name='assignment_submitted_by', on_delete=models.DO_NOTHING)
    assessed_by = models.ForeignKey(Staff, related_name='assignment_assessed_by', on_delete=models.DO_NOTHING, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    def __str__(self) -> str:
        return self.subject.name+" "+'Assignment submitted by' + " " +self.submitted_by.admin.username


class Submitted_Test(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    submitted_status = models.BooleanField(null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True, null=True)
    submitted_test_text = models.TextField(blank=True, null=True)
    submitted_test_file = models.FileField(upload_to='media/files/submitted_assignment_files', max_length=150, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    submitted_by = models.ForeignKey(Student, related_name='test_submitted_by', on_delete=models.DO_NOTHING)
    assessed_by = models.ForeignKey(Staff, related_name='test_assessed_by', on_delete=models.DO_NOTHING, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.subject.name+" "+'Test submitted by' + " " +self.submitted_by.admin.username

class Submitted_Examination(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    submitted_exam_text = models.TextField(blank=True, null=True)
    submitted_status = models.BooleanField(null=True, blank=True)
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE, blank=True, null=True)
    submitted_exam_file = models.FileField(upload_to='media/files/submitted_examination_files', max_length=150, blank=True, null=True)
    subject = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    submitted_by = models.ForeignKey(Student, related_name='examination_submitted_by', on_delete=models.DO_NOTHING)
    assessed_by = models.ForeignKey(Staff, related_name='examination_assessed_by', on_delete=models.DO_NOTHING, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)

    def __str__(self) -> str:
        return self.subject.name + " " + 'Examination submitted by' + " " + self.submitted_by.admin.username

class CBT(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True)
    studentclass = models.ForeignKey(StudentClass, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=50)
    duration = models.IntegerField()
    questions = models.IntegerField()
    marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class CBTQ(models.Model):
    cbt = models.ForeignKey(CBT, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000, null=True, blank=True)
    marks=models.PositiveIntegerField(null=True, blank = True)
    option1 = models.CharField(max_length=100, null=True, blank=True)
    option2 = models.CharField(max_length=100, null=True, blank=True)
    option3 = models.CharField(max_length=100, null=True, blank=True)
    option4 = models.CharField(max_length=100, null=True, blank=True)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answers=models.CharField(choices=cat,max_length=200)
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
class CBTR(models.Model):
    cbt = models.ForeignKey(CBT, on_delete=models.CASCADE)
    student = models.ForeignKey( Student, on_delete=models.CASCADE)
    score = models.FloatField( null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class BulkEmail(models.Model):
    message = models.CharField(max_length=1000)
    sent_to = models.CharField(max_length=50)
    sent_by = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
