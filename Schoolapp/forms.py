from django import forms
from django.contrib.auth.forms import UserCreationForm
from Schoolapp.models import Prospective_Candidate
from users.models import *

class Prospective_UserForm(UserCreationForm):
    username = forms.CharField(max_length=50, label="Username", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Username"}))
    fullname = forms.CharField(max_length=50, label='Full Name', widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder': 'Full Name'}))
    password1 = forms.CharField(max_length=50, label="Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Password"}))
    password2 = forms.CharField(max_length=50, label="Confirm Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Confirm Password"}))


    email = forms.EmailField(label='Email Address', max_length=500, required=True, widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder' : 'Email Address'}))
    phone_number = forms.CharField(label='Phone Number', max_length=500, required=True, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Phone Number',
    }))

    status = [
        ('parent', 'Parent'),
        ('student', 'Student'),
        ('guardian', 'Guardian'),
    ]
    user_status = forms.ChoiceField(choices=status, required=False, widget=forms.Select(attrs={
        'class' : 'form-control',
    }))

    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'fullname', 'phone_number', 'user_status']
class Prospective_UsersForm(UserCreationForm):
    username = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"First Name"}))
    first_name = forms.CharField(max_length=50, label="Middle Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Middle Name"}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Last Name"}))
    email = forms.CharField(max_length=50, label="Email", widget=forms.EmailInput(attrs = {'class' : 'form-control', 'placeholder':"Email"}))
    password1 = forms.CharField(max_length=50, label="Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Password"}))
    password2 = forms.CharField(max_length=50, label="Confirm Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Confirm Password"}))
    age = forms.IntegerField(required=False, label='Age', widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Age'}))
    address = forms.CharField(max_length=80, label="Address", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Address"}))
    parent_phone_number = forms.CharField(max_length=15, label="Parent or Guardian Phone Number",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Parent or Guardian Phone Number"}))
    user_type = forms.CharField(widget=forms.HiddenInput(attrs={'value':'prospective',}))  
    date_of_birth = forms.DateField(label="Date Of Birth", widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD format'}))

    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []

    try:
       sessions =  SessionYearModel.objects.all()
       sessions_list =[]
       for session in sessions:
            single_session = (session.id, str(session.session_start_year)+ 'to' + str(session.session_end_year))
            sessions_list.append(single_session)
    except:
        sessions_list = []

    gender_type = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    
    try:
        departments = Department.objects.all()
        departments_list = []
        for department in departments:
            single_department = (department.id, department.name)
            departments_list.append(single_department)
    except:
        departments_list = []

    parent_name = forms.CharField(max_length=500, label="Parent or Guardian Name",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Parent or Guardian Name"}))
    parentstatus = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ]
    parent_status = forms.ChoiceField(choices=parentstatus, required=True, label="Parent Status",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Parent Status"}))
    gender = forms.ChoiceField(choices=gender_type, label="Gender",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Gender"}))
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    department = forms.ChoiceField(label="Department", required=False, choices = departments_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Department"}))
    # session_joined = forms.ChoiceField(label="Session Joined/Joining", required=False, choices = sessions_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Session Joined/Joining"}))
    # profile_pic = forms.FileField(label="Profile Picture", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Profile Picture"}))

    class Meta:
        model = CustomUser
        fields=['username', 'first_name', 'last_name', 'email', 'password1', 'password2','department','student_class','gender', 'address', 'user_type']
        
        label = {
            'password1' : 'Password',
            'password2' : 'Confirm Password',
        }