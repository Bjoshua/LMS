from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
# from users.models import Department, Staff, StudentClass, SessionYearModel, CustomUser
from django.contrib.auth import authenticate, get_user_model, password_validation
from users.models import *
from Schoolapp.models import *
from django.core.exceptions import ValidationError

class AddStudentForm(UserCreationForm):
    username = forms.CharField(max_length=50, label="Userame", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Username"}))
    first_name = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"First Name"}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Last Name"}))
    email = forms.CharField(max_length=50, label="Email", widget=forms.EmailInput(attrs = {'class' : 'form-control', 'placeholder':"Email"}))
    password1 = forms.CharField(max_length=50, label="Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Password"}))
    password2 = forms.CharField(max_length=50, label="Confirm Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Confirm Password"}))
    age = forms.IntegerField(required=False, label='Age', widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Age'}))
    address = forms.CharField(max_length=80, label="Address", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Address"}))
    user_type = forms.CharField(widget=forms.HiddenInput(attrs={'value':'student',}))  
    # date_of_birth = forms.DateField(label="Date Of Birth", widget=forms.SelectDateWidget(attrs={'class':'form-select', 'placeholder':'YYYY-MM-DD format'}))

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
    try:
        subjects = Subjects.objects.all()
        subjects_list = []
        for subject in subjects:
            single_subject = (subject.id, subject.name)
            subjects_list.append(single_subject)
    except:
        subjects_list = []


    parent_name = forms.CharField(max_length=500, label="Parent or Guardian Name",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Parent or Guardian Name"}))
    parentstatus = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ]
    parent_status = forms.ChoiceField(choices=parentstatus, required=True, label="Parent Status",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Parent Status"}))
    parent_phone_number = forms.CharField(max_length=15, label="Parent or Guardian Phone Number",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Parent or Guardian Phone Number"}))
    gender = forms.ChoiceField(choices=gender_type, label="Gender",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Gender"}))
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    department = forms.ChoiceField(label="Department", required=False, choices = departments_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Department"}))
    # subject = forms.CharField(label="Subjects", required=False, widget=forms.MultiValueField(fields= [subjects_list}))
    session_joined = forms.ChoiceField(label="Session Joined/Joining", required=False, choices = sessions_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Session Joined/Joining"}))
    # profile_pic = forms.FileField(label="Profile Picture", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Profile Picture"}))

    class Meta:
        model = CustomUser
        fields=['username', 'first_name', 'last_name', 'email', 'password1', 'password2','session_joined','department','student_class','gender', 'address', 'user_type']
        
        label = {
            'password1' : 'Password',
            'password2' : 'Confirm Password',
        }
        

class AddStaffForm(UserCreationForm):
    username = forms.CharField(max_length=50, label="Username", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Username"}))
    first_name = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"First Name"}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Last Name"}))
    email = forms.CharField(max_length=50, label="Email", widget=forms.EmailInput(attrs = {'class' : 'form-control', 'placeholder':"Email"}))
    password1 = forms.CharField(max_length=50, label="Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Password"}))
    password2 = forms.CharField(max_length=50, label="Confirm Password", widget=forms.PasswordInput(attrs = {'class' : 'form-control', 'placeholder':"Confirm Password"}))
    phone_number = forms.CharField(max_length=15, label="Phone Number",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Phone Number"}))
    address = forms.CharField(max_length=80, label="Address", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Address"}))
    user_type = forms.CharField(widget=forms.HiddenInput(attrs={'value':'staff',}))  

    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []
           
    gender_type = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = forms.ChoiceField(choices=gender_type, label="Gender",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Gender"}))
    # student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    # profile_pic = forms.FileField(label="Profile Picture", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Profile Picture"}))

    class Meta:
        model = CustomUser
        fields=['username', 'first_name', 'last_name', 'email', 'password1', 'password2','gender', 'address', 'user_type']

        label = {
            'password1' : 'Password',
            'password2' : 'Confirm Password',
        }

class AdminEditStaffProfileForm(forms.Form):
    username = forms.CharField(max_length=50, label="Username", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Username"}))
    first_name = forms.CharField(max_length=50, label="First Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"First Name"}))
    last_name = forms.CharField(max_length=50, label="Last Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Last Name"}))
    email = forms.CharField(max_length=50, label="Email", widget=forms.EmailInput(attrs = {'class' : 'form-control', 'placeholder':"Email"}))
    phone_number = forms.CharField(max_length=15, label="Phone Number",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Phone Number"}))
    address = forms.CharField(max_length=80, label="Address", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Address"}))

    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []
           
    gender_type = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = forms.ChoiceField(choices=gender_type, label="Gender",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Gender"}))
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))

class AdminEditLectureForm(forms.Form):
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            format = (subject.id, subject.name)
            subject_list.append(format)        
    except: 
        subject_list = []
    
    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []
        
    try:
        staffs = Staff.objects.all()
        staff_list = []
        for staff in staffs:
            single_class = (staff.id, staff.admin.first_name+staff.admin.last_name)
            staff_list.append(single_class)
    except:
        staff_list = []

        
    subject = forms.ChoiceField(choices=subject_list, label="Subject",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Subject"}))
    form_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    created_by = forms.ChoiceField(label="Created By", required=False, choices = staff_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Created By"}))
    lecture_file = forms.FileField(label="Lecture File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture File"}))
    lecture_video = forms.FileField(label="Lecture Video", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture Video"}))
    lecture_ppt = forms.FileField(label="Lecture PPT", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture PPT"}))
    lecture_text = forms.CharField(max_length=500, label="Lecture Note",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Lecture Note"}))
    heading = forms.CharField(max_length=500, label="Lecture Topic",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Lecture Topic"}))



class StaffEditLectureForm(forms.Form):
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            format = (subject.id, subject.name)
            subject_list.append(format)        
    except: 
        subject_list = []
    
    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []
        
    subject = forms.ChoiceField(choices=subject_list, label="Subject",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Subject"}))
    form_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    lecture_file = forms.FileField(label="Lecture File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture File"}))
    lecture_video = forms.FileField(label="Lecture Video", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture Video"}))
    lecture_ppt = forms.FileField(label="Lecture PPT", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture PPT"}))
    lecture_text = forms.CharField(max_length=500, label="Lecture Note",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Lecture Note"}))
    heading = forms.CharField(max_length=500, label="Lecture Topic",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Lecture Topic"}))

    
class EditEventForm(forms.Form):
    event_name = forms.CharField(max_length=800, label="Event Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Event Name"}))
    event_description = forms.CharField(max_length=1500, label="Event Description",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'placeholder':"Event Description"}))
    event_date = forms.DateField(label="Event Date",required=True, widget=forms.DateTimeInput(attrs = {'class' : 'form-control', 'type':"date"}))
    event_time = forms.TimeField(label="Event Time",required=True, widget=forms.DateTimeInput(attrs = {'class' : 'form-control', 'type':"time"}))
    event_location = forms.CharField(max_length=150, label="Event Location",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Event Location"}))
    image_description = forms.FileField(label="Event Image",required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Event Image", 'accept':'image/*'}))
    

class StaffUpdateProfileForm(forms.Form):
    address = forms.CharField(max_length=80, label="Address", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Address"}))
    phone_number = forms.CharField(max_length=15, label="Phone Number",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Phone Number"}))

class EventForm(forms.ModelForm):
    event_name = forms.CharField(max_length=800, label="Event Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Event Name"}))
    event_description = forms.CharField(max_length=1500, label="Event Description",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'placeholder':"Event Description"}))
    event_date = forms.DateField(label="Event Date",required=True, widget=forms.DateTimeInput(attrs = {'class' : 'form-control', 'placeholder':"YYYY-MM-DD Format", 'type': "date"}))
    event_time = forms.TimeField(label="Event Time",required=True, widget=forms.DateTimeInput(attrs = {'class' : 'form-control', 'placeholder':"HH:MM:SS Format", 'type': "time"}))
    event_location = forms.CharField(max_length=150, label="Event Location",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Event Location"}))
    image_description = forms.FileField(label="Event Image",required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Event Image"}))

    class Meta:
        model = UpcommingEvents
        fields = ['event_name', 'event_description', 'event_date', 'event_time', 'event_location', 'image_description']

        
class AddAssignment(forms.Form):
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            format = (subject.id, subject.name)
            subject_list.append(format)        
    except: 
        subject_list = []
       
    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []
    try:
        department = Department.objects.all()
        department_list = []
        for departments in department:
            single_department = (departments.id, departments.name)
            department_list.append(single_department)
    except:
        department_list = []
 
        
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    department_id = forms.ChoiceField(label="Department", required=False, choices = department_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Department"}))
    subject = forms.ChoiceField(choices=subject_list, label="Subject",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Subject"}))
    question_file = forms.FileField(label="Assignment File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Assignment File"}))
    question_text = forms.CharField(max_length=500, label="Assignment Question",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Assignment Question"}))
    
class AddTest(forms.Form):
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            format = (subject.id, subject.name)
            subject_list.append(format)        
    except: 
        subject_list = []
     
    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []

    test = [    
        ('1st', 'First CA Test'),    
        ('2nd', 'Second CA Test'),
        ('3rd', 'Third CA Test'),
    ]
       
    test_name = forms.ChoiceField(choices=test, label="Test Type",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Test Type"}))
    subject = forms.ChoiceField(choices=subject_list, label="Subject",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Subject"}))
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    question_file = forms.FileField(label="Test File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Test File"}))
    question_text = forms.CharField(max_length=500, label="Test Question",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Test Question"}))

class studenttest(forms.Form):
    question_file = forms.FileField(label="Test Answer File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Test Answer File"}))
    question_text = forms.CharField(max_length=500, label="Test Answer",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Test Answer"}))    

class studentassignment(forms.Form):
    question_file = forms.FileField(label="Assignment Answer File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Assignment Answer File"}))
    question_text = forms.CharField(max_length=500, label="Assignment Answer",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Assignment Answer"}))    

class studentexam(forms.Form):
    question_file = forms.FileField(label="Examination Answer File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Examination Answer File"}))
    question_text = forms.CharField(max_length=500, label="Examination Answer",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Examination Answer"}))    

class AddExamination(forms.Form):
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            format = (subject.id, subject.name)
            subject_list.append(format)        
    except: 
        subject_list = []

    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []
        
        
    subject = forms.ChoiceField(choices=subject_list, label="Subject",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Subject"}))
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    question_file = forms.FileField(label="Examination File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Examination File"}))
    question_text = forms.CharField(max_length=500, label="Examination Question",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Examination Question"}))
    
class AddLecture(forms.Form):
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            format = (subject.id, subject.name)
            subject_list.append(format)        
    except: 
        subject_list = []
    
    try:
        student_classes = StudentClass.objects.all()
        class_list = []
        for classes in student_classes:
            single_class = (classes.id, classes.name)
            class_list.append(single_class)
    except:
        class_list = []
        
    subject = forms.ChoiceField(choices=subject_list, label="Subject",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Subject"}))
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))
    lecture_file = forms.FileField(label="Lecture File", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture File"}))
    lecture_video = forms.FileField(label="Lecture Video", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture Video"}))
    lecture_ppt = forms.FileField(label="Lecture PPT", required=False, widget=forms.FileInput(attrs = {'class' : 'form-control', 'placeholder':"Lecture PPT"}))
    lecture_text = forms.CharField(max_length=500, label="Lecture Note",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Lecture Note"}))
    lecture_heading = forms.CharField(max_length=500, label="Lecture Topic",required=True, widget=forms.Textarea(attrs = {'class' : 'form-control', 'cols':10, 'rows':5,'placeholder':"Lecture Topic"}))
    
    
class Score(forms.Form):
    age = forms.FloatField(required=False, label='Score', widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Score'}))
 
   
class AddSubject(forms.Form):
    try:
        departments = Department.objects.all()
        department_list = []
        for subject in departments:
            format = (subject.id, subject.name)
            department_list.append(format)        
    except: 
        department_list = []
        
    try:
        # aaa=CustomUser.objects.filter(user_type='2')
        staffs = Staff.objects.all()
        staff_list = []
        for staff in staffs:
            format = (staff.id, staff.admin.first_name+' '+staff.admin.last_name)
            staff_list.append(format)        
    except: 
        staff_list = []
        
    name = forms.CharField(max_length=50, label="Name", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Name"}))
    department = forms.ChoiceField(choices=department_list, label="Department",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Department"}))
    staff = forms.ChoiceField(choices=staff_list, label="Staff",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"staff_list"}))
    
class EditStudentForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class":"form-control"}))
    age = forms.IntegerField(required=False, label='Age', widget=forms.NumberInput(attrs={'class' : 'form-control', 'placeholder':'Age'}))
    # date_of_birth = forms.DateField(label="Date Of Birth", widget=forms.DateInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD format'}))
    parents_phone_number = forms.CharField(max_length=15, label="Parent or Guardian Phone Number",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Parent or Guardian Phone Number"}))

    
    try:
        classes = StudentClass.objects.all()
        class_list = []
        for classs in classes:
            single_class = (classs.id, classs.name)
            class_list.append(single_class)
    except:
        class_list = []

    try:
        session_years = SessionYearModel.objects.all()
        session_year_list = []
        for session_year in session_years:
            single_session_year = (session_year.id, str(session_year.session_start_year)+" to "+str(session_year.session_end_year))
            session_year_list.append(single_session_year)            
    except:
        session_year_list = []
    
    try:
        departments = Department.objects.all()
        departments_list = []
        for department in departments:
            single_department = (department.id, department.name)
            departments_list.append(single_department)
    except:
        departments_list = []

    
    gender_list = (
        ('Male','Male'),
        ('Female','Female')
    )
    parent_name = forms.CharField(max_length=500, label="Parent or Guardian Name",required=True, widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Parent or Guardian Name"}))
    parentstatus = [
        ('father', 'Father'),
        ('mother', 'Mother'),
        ('guardian', 'Guardian'),
    ]
    parent_status = forms.ChoiceField(choices=parentstatus, required=True, label="Parent Status",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Parent Status"}))
    department = forms.ChoiceField(label="Department", required=False, choices = departments_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Department"}))
    gender = forms.ChoiceField(label="Gender", choices=gender_list, widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id = forms.ChoiceField(label="Session Year", choices=session_year_list, widget=forms.Select(attrs={"class":"form-control"}))
    student_class = forms.ChoiceField(label="Class", required=False, choices = class_list, widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"Class"}))

    
class AddClass(forms.Form):
    try:
        # aaa=CustomUser.objects.filter(user_type='2')
        staffs = Staff.objects.all()
        staff_list = []
        for staff in staffs:
            format = (staff.id, staff.admin.first_name+' '+staff.admin.last_name)
            staff_list.append(format)        
    except: 
        staff_list = []
        
    name = forms.CharField(max_length=50, label="Name(e.g SS1A, JSS3B)", widget=forms.TextInput(attrs = {'class' : 'form-control', 'placeholder':"Name"}))
    staff = forms.ChoiceField(choices=staff_list, label="Staff",  widget=forms.Select(attrs = {'class' : 'form-control', 'placeholder':"staff_list"}))                 

class AddSubjectForm(forms.Form):
    name = forms.CharField(max_length=50, label='Subject Name', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Subject's name"}))
    try:
        staffs = Staff.objects.all()
        staff_list = []
        for staff in staffs:
            single_staff = (staff.id, staff.admin.username)
            staff_list.append(single_staff)
    except:
        staff_list = []   

    try:
        staffs = StudentClass.objects.all()
        class_list = []
        for staff in staffs:
            single_staff = (staff.id, staff.name)
            class_list.append(single_staff)
    except:
        class_list = []   

    try:
        departments = Department.objects.all()
        department_list = []
        for department in departments:
            single_department = (department.id, department.name)
            department_list.append(single_department)
    except:
        department_list = [] 
    department = forms.ChoiceField(label='Department', choices= department_list, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    staff = forms.ChoiceField(label='Teacher', choices= staff_list,required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    # classs = forms.ChoiceField(label='Subject Class', choices= class_list,required=True, widget=forms.Select(attrs={'class': 'form-control'}))

class EditSubjectForm(forms.Form):
    name = forms.CharField(max_length=50, label='Subject Name', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Subject's name"}))
    try:
        staffs = Staff.objects.all()
        staff_list = []
        for staff in staffs:
            single_staff = (staff.id, staff.admin.username)
            staff_list.append(single_staff)
    except:
        staff_list = []   

    try:
        staffs = StudentClass.objects.all()
        class_list = []
        for staff in staffs:
            single_staff = (staff.id, staff.name)
            class_list.append(single_staff)
    except:
        class_list = []   

    try:
        departments = Department.objects.all()
        department_list = []
        for department in departments:
            single_department = (department.id, department.name)
            department_list.append(single_department)
    except:
        department_list = [] 
    department = forms.ChoiceField(label='Department', choices= department_list, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    staff = forms.ChoiceField(label='Teacher', choices= staff_list,required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    # classs = forms.ChoiceField(label='Subject Class', choices= class_list,required=True, widget=forms.Select(attrs={'class': 'form-control'}))




class AddClassForm(forms.Form):
    name = forms.CharField(max_length=6, label='Name(example SS1A, JSS3B)', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Class Name"}))
    try:
        staffs = Staff.objects.all()
        staff_list = []
        for staff in staffs:
            single_staff = (staff.id, staff.admin.username)
            staff_list.append(single_staff)
    except:
        staff_list = []
    staff = forms.ChoiceField(label='Class Teacher', choices= staff_list,required=True, widget=forms.Select(attrs={'class': 'form-control'}))

class CreateCbtForm(forms.Form):
    name = forms.CharField(max_length=30, label='Name(example CBT1, CBT2)', widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': "CBT Name"}))
    try:
        subjects = Subjects.objects.all()
        subject_list = []
        for subject in subjects:
            single_subject = (subject.id, subject.name)
            subject_list.append(single_subject)
    except:
        subject_list = [] 

    try:
        classes = StudentClass.objects.all()
        class_list = []
        for classs in classes:
            single_class = (classs.id, classs.name)
            class_list.append(single_class)
    except:
        class_list = []
    subject = forms.ChoiceField(label='Subject', choices= subject_list, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    classs = forms.ChoiceField(label='Class', choices= class_list,required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    duration = forms.IntegerField(label='Duration', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    questions = forms.IntegerField(label='Questions', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    marks = forms.IntegerField(label='Marks', required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
class QuestionForm(forms.ModelForm):
    class Meta:
        model=CBTQ
        fields=['marks','question','option1','option2','option3','option4','answers']
        widgets = {
            'question': forms.Textarea(attrs={'rows': 3, 'cols': 50})
        }

     