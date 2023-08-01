from django.shortcuts import render
# from users.forms import AddStudentForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from users.EmailBackEnd import EmailBackEnd
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from Schoolapp.models import *
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from chat.models import Room, Messages
from .forms import *
from datetime import datetime
from django.core.mail import send_mail
def djangoadmin(request):
    return admin.sites.urls

@login_required(login_url='login')
def admin_home(request):
    students = Student.objects.all()
    staffs = Staff.objects.all()
    subjects = Subjects.objects.all()
    departments = Department.objects.all()
    sessions = SessionYearModel.objects.all()
    classes = StudentClass.objects.all()
    context = {
        'students':students,
        'staffs':staffs,
        'subjects':subjects,
        'departments':departments,
        'sessions':sessions,
        'classes':classes,
    }
    return render(request, 'profiles/Admin Templates/home.html', context)

@login_required(login_url='login')
def admin_profile(request):
    user = request.user
    return render(request, "profiles/Admin Templates/profile_update.html", {'user':user})
def admin_profile_update(request):
    if request.method == "POST":
        user = request.user
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            if password:
                user.set_password(password)
            user.save()
            adminn = AdminHOD.objects.filter(admin=user).exists()
            print(adminn)
            if len(request.FILES) != 0:
                picture = request.FILES.get('picture')
                fs = FileSystemStorage()
                filename = fs.save(picture.name, picture)
                picture_url = fs.url(filename)
                if adminn:
                    adminnn = AdminHOD.objects.get(admin=user)
                    adminnn.profile_pic = picture_url
                    adminnn.save()
                else:
                    create_admin = AdminHOD.objects.create(admin=request.user, profile_pic=picture_url)
                    create_admin.save()
                print(create_admin)
            messages.success(request, 'Profile Updated Succesfully')
            return redirect(admin_home)
        except:
            messages.error(request, 'Profile Update Failed')
            return redirect(admin_profile)

    else:
        messages.error(request, 'Method not allowed')
        return redirect(admin_profile_update)


@login_required(login_url='login')
def manage_staff(request):
    staffs = Staff.objects.all()
    form = AddStaffForm()
    if request.method == 'POST':
        form = AddStaffForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            for userss in CustomUser.objects.all():
                if email == userss.email:
                    messages.error(request, "A user with that Email department_id exists")
                    return redirect('add_staff')
                    break
                else:
                    form.save()
                    user_types = form.cleaned_data['user_type']
                    user = form.save()
                    username = form.cleaned_data['username']
                    print(user_types)
                    
                    address = form.cleaned_data['address']
                    # student_class = form.cleaned_data('student_class')
                    gender = form.cleaned_data['gender']

                    staff_class = request.POST.get('student_class')
                    if len(request.FILES) != 0:
                        picture = request.FILES.get('picture')
                        fs = FileSystemStorage()
                        filename = fs.save(picture.name, picture)
                        picture_url = fs.url(filename)
                    phone_number = request.POST.get('phone_number')

                    try:
                        # user = CustomUser.objects.create(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3, is_active=True)
                        # staff_classs = StudentClass.objects.get(id=staff_class)

                        staff = Staff.objects.create(admin=user, address= address, profile_pic=picture_url, user_type='2', phone_number=phone_number)
                        staff.save()

                        messages.success(request, f"Staff {username} Added Succesfully")
                        return redirect(manage_staff)
                    except:
                        messages.error(request, "Failed to Add Staff!")
                        return redirect(manage_staff)
    context = {
        "staffs": staffs,
        "form":form,
    }
    return render(request,'profiles/Admin Templates/manage-staff.html', context)
def admin_staff_edit_profile(request, user_id):
    user=CustomUser.objects.get(id=user_id)
    staff = user.staff
    form = AdminEditStaffProfileForm()
    form.fields['address'].initial = user.staff.address
    form.fields['email'].initial = user.email
    form.fields['phone_number'].initial = staff.phone_number
    form.fields['first_name'].initial = user.first_name
    form.fields['last_name'].initial = user.last_name
    form.fields['username'].initial = user.username
    form.fields['student_class'].initial = staff.form_class
    if request.method == 'POST':
        form = EditStudentForm(request.POST, request.FILES)
        
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            gender = request.POST.get('gender')
            student_class = request.POST.get('student_class')
            if len(request.FILES) != 0:
                picture = request.FILES.get('picture')
                fs = FileSystemStorage()
                filename = fs.save(picture.name, picture)
                picture_url = fs.url(filename)
                staff.profile_pic=picture_url
            classss = StudentClass.objects.get(id=student_class)
            
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            staff.address = address
            staff.parents_phone_number = phone_number
            staff.gender = gender
            staff.form_class = classss
            user.save()
            staff.save()
            messages.success(request, f"Sucessfully updated {staff.admin.username}'s profile.")
            return redirect('manage_staff')
        except:
            messages.error(request, f"Profile Update Failed.")
            return redirect('manage_staff')
        
    context = {'form':form}
    return render(request, 'profiles/Admin Templates/edit_staff.html', context)

@login_required(login_url='login')
def delete_staff(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    user = CustomUser.objects.get(id=staff.admin.id)
    try:
        staff.delete()
        user.delete()
        messages.success(request, "Staff deleted")
        return redirect(manage_staff)
    except:
        messages.error(request, "Staff failed to delete try again")
        return redirect(manage_staff)
def manage_prospective(request):
    staffs = Prospective_Candidate.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request,'profiles/Admin Templates/prospective_user.html', context)
@login_required(login_url='login')
def manage_stud(request):
    students = Student.objects.all()
    form = AddStudentForm()
    if request.method == "POST":
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            for userss in CustomUser.objects.all():
                if email == userss.email:
                    messages.error(request, "A user with that Email address exists")
                    return redirect(manage_stud)
                    break
                else:
                    user_types = form.cleaned_data['user_type']
                    user = form.save()
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    username = form.cleaned_data['username']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password1']
                    address = form.cleaned_data['address']
                    session_year_id = form.cleaned_data['session_joined']
                    phone_number = request.POST.get('parent_phone_number')
                    # student_class = form.cleaned_data('student_class')
                    gender = form.cleaned_data['gender']

                    student_class = request.POST.get('student_class')
                    parent_name = request.POST.get('parent_name')
                    age = request.POST.get('age')
                    date_of_birth = request.POST.get('date_of_birth')
                    parent_status = request.POST.get('parent_status')
                    if len(request.FILES) != 0:
                        picture = request.FILES.get('picture')
                        fs = FileSystemStorage()
                        filename = fs.save(picture.name, picture)
                        picture_url = fs.url(filename)
                    else:
                        picture_url = None
                        
                    department_id = request.POST.get('department')       
                    try:
                        student_classs = StudentClass.objects.get(id=student_class)
                        department_ids = Department.objects.get(id=department_id)
                        session_year_ids = SessionYearModel.objects.get(id=session_year_id)
                        student = Student.objects.create(admin=user, parent_name=parent_name, parent_status=parent_status, address= address, student_class=student_classs, department_id=department_ids, session_year_id=session_year_ids, gender=gender, parents_phone_number=phone_number, age=age, profile_pic=picture_url, user_types='3', date_of_birth=date_of_birth)
                        student.save()
                        chatroom_name = str(student_classs)+ " Chat Room"
                        chat_room = Room.objects.get(name=chatroom_name)
                        students = Student.objects.filter(student_class=student.student_class)
                        if chat_room:
                            chat_room.members.set(students)
                            messages.success(request, f"Hello {username}, you have been Added Successfully! Best Of Luck in GVIC")
                            return redirect(manage_stud)
                    
                    except:
                        messages.error(request, "Failed to Add Student!")
                        return redirect(manage_stud)
    context = {
        "form":form,
        "students":students,
    }
    return render(request,'profiles/Admin Templates/manage-stud.html', context)

def admin_student_edit_profile(request, user_id):
    user=CustomUser.objects.get(id=user_id)
    student = user.student
    form = EditStudentForm()
    form.fields['address'].initial = student.address
    form.fields['email'].initial = user.email
    form.fields['parents_phone_number'].initial = student.parents_phone_number
    form.fields['parent_name'].initial = student.parent_name
    form.fields['first_name'].initial = user.first_name
    form.fields['last_name'].initial = user.last_name
    form.fields['username'].initial = user.username
    form.fields['session_year_id'].initial = student.session_year_id
    form.fields['gender'].initial = student.gender
    form.fields['student_class'].initial = student.student_class
    form.fields['age'].initial = student.age
    # form.fields['date_of_birth'].initial = student.date_of_birth
    form.fields['department'].initial = student.department_id
    form.fields['student_class'].initial = student.student_class
    if request.method == 'POST':
        form = EditStudentForm(request.POST)
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')        
            address = request.POST.get('address')
            session_year_id = request.POST.get('session_joined')
            phone_number = request.POST.get('parents_phone_number')
            gender = request.POST.get('gender')

            student_class = request.POST.get('student_class')
            
            parent_name = request.POST.get('parent_name')
            age = request.POST.get('age')
            date_of_birth = request.POST.get('date_of_birth')
            parent_status = request.POST.get('parent_status')
            if len(request.FILES) != 0:
                picture = request.FILES.get('picture')
                fs = FileSystemStorage()
                filename = fs.save(picture.name, picture)
                picture_url = fs.url(filename)
                student.profile_pic = picture_url
                # student.save()
            print(session_year_id)
            department_id = request.POST.get('department')
            department = Department.objects.get(id=department_id)
            session_year_ids = SessionYearModel.objects.get(id=session_year_id)
            classss = StudentClass.objects.get(id=student_class)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            student.address = address
            student.session_year_id = session_year_ids
            student.parents_phone_number = phone_number
            student.gender = gender
            student.student_class = classss
            student.parent_name = parent_name
            student.age = age
            if date_of_birth:
                student.date_of_birth = date_of_birth
            student.parent_status = parent_status
            student.department_id = department
            user.save()
            student.save()
            messages.success(request, f"Sucessfully updated {student.admin.first_name} {student.admin.last_name}'s profile.")
            return redirect(manage_stud)
        except:
            messages.error(request, f"Profile Update Failed.")
            return redirect(manage_stud)
        
    context = {'form':form}
    return render(request, 'profiles/Admin Templates/edit_student.html', context)

def delete_student(request, student_id):
    student = Student.objects.get(id=student_id)
    stud_user = CustomUser.objects.get(id = student.admin.id)
    try:
        student.delete()
        stud_user.delete()
        messages.success(request, 'Student deleted')
        return redirect(manage_stud)
    except:
        messages.error(request, 'Student failed to Delete try again')
        return redirect(manage_stud)

def manage_sub(request):
    subjects = Subjects.objects.all()
    form = AddSubjectForm()
    if request.method == "POST":
        form = AddSubjectForm(request.POST)
        name = request.POST.get('name')
        get_department = request.POST.get('department')
        get_staff = request.POST.get('staff')
        # classss = request.POST.get('classs')
        department = Department.objects.get(id=get_department)
        staffs = Staff.objects.get(id=get_staff)
        staff = CustomUser.objects.get(id=staffs.admin.id)
        # sstaff = StudentClass.objects.get(id=classss)
        try:
            subject = Subjects(name=name, staff_id=staff, department_id=department)
            subject.save()
            messages.success(request, 'Subject Added Succesfully')
            return redirect(manage_sub)    
        except:
            messages.error(request, 'Subject Failed to Add, Try again')
            return redirect(manage_sub) 
    context = {
        "subjects":subjects,
        "form":form,
    } 
    return render(request,'profiles/Admin Templates/manage-subjects.html', context)

def edit_sub(request, subject_id):
    form = EditSubjectForm()
    subject = Subjects.objects.get(id=subject_id)
    
    form.fields['name'].initial = subject.name
    # form.fields['classs'].initial = subject.subj_class
    form.fields['department'].initial = subject.department_id
    form.fields['staff'].initial = subject.staff_id
    
    if request.method == "POST":
        # form = AddSubjectForm(request.POST)
        name = request.POST.get('name')
        get_department = request.POST.get('department')
        get_staff = request.POST.get('staff')
        classss = request.POST.get('classs')
        department = Department.objects.get(id=get_department)
        staffs = Staff.objects.get(id=get_staff)
        staff = CustomUser.objects.get(id=staffs.admin.id)
        # sstaff = StudentClass.objects.get(id=classss)
        
        subject.name = name
        subject.department_id=department
        subject.department_id=department
        subject.staff_id=staff
        # subject.subj_class=sstaff
        subject.save()
        messages.success(request, 'Editing Subject successful')    
        return redirect('manage_sub')
    return render(request, 'profiles/Admin Templates/edit_sub.html', {'form': form})

def delete_sub(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, 'Subject deleted')
        return redirect(manage_sub)
    except:
        messages.error(request, 'Subject failed to Delete try again')
        return redirect(manage_sub)

@login_required(login_url='login')
def manage_class(request):
    classes = StudentClass.objects.all()
    form = AddClass()
    # exclude_teacher = Staff.objects.get(id=2)
    # form.fields['staff'].initial = exclude_teacher
    if request.method == "POST":
        form = AddClass(request.POST)
        name = request.POST.get('name')
        teacher = request.POST.get('staff')
        staff = Staff.objects.get(id=teacher)
        user_staff = CustomUser.objects.get(id=staff.admin.id)
        staff_occupied = StudentClass.objects.filter(staff_id=user_staff).exists()
        if staff_occupied:
            messages.error(request, f"{user_staff.first_name} {user_staff.last_name} is already assigned to a class and can't be assigned to another class")
            return redirect(manage_class)
        else:
            try:
                create_class = StudentClass.objects.create(name=name, staff_id=user_staff)
                create_class.save()
                chatroom_name = name+ " Chat Room"
                chat_room = Room.objects.create(name=chatroom_name, admin=staff)
                chat_room.save()
                messages.success(request, 'Class created Successfully')
                return redirect(manage_class)
            except:
                messages.error(request, 'Class creation Failed')
                return redirect(manage_class)
    context ={
        "form":form,
        "classes":classes,
    }
    return render(request, 'profiles/Admin Templates/manage-class.html', context)

@login_required(login_url='login')
def edit_class(request, class_id):
    form = AddClassForm()
    get_class = StudentClass.objects.get(id=class_id)
    form.fields['name'].initial = get_class.name
    form.fields['staff'].initial = get_class.staff_id
    if request.method == "POST":
        form = AddSubjectForm(request.POST)
        name = request.POST.get('name')
        get_staff = request.POST.get('staff')
        staffs = Staff.objects.get(id=get_staff)
        staff = CustomUser.objects.get(id=staffs.admin.id)
        staff_occupied = StudentClass.objects.filter(staff_id=staff).exists()
        if staff_occupied:
            messages.error(request, f"{staff.first_name} {staff.last_name} is already assigned to a class and can't be assigned to another class")
            return redirect(manage_class)
        else:
            try:
                get_class.name = name
                get_class.staff_id=staff
                get_class.save()
                messages.success(request, f'Editing Class {get_class.name} successful')    
                return redirect('manage_class')
            except:
                messages.error(request, f'Editing Class {get_class.name} Failed')    
                return redirect('manage_class') 
    return render(request, 'profiles/Admin Templates/edit_class.html', {'form': form})
def delete_class(request, class_id):
    classs = StudentClass.objects.get(id=class_id)
    # chat_room_name = classs.name+ " Chat Room"
    # chat_room = Room.objects.get(name= chat_room_name)
    try:
        classs.delete()
        # chat_room.delete()
        messages.success(request, 'Class deleted')
        return redirect(manage_class)
    except:
        messages.error(request, 'Class failed to Delete try again')
        return redirect(manage_class)
def sessions(request):
    all_sessions = SessionYearModel.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        session_start_year = request.POST.get("start_year")
        session_end_year = request.POST.get("end_year")
        try:
            session = SessionYearModel.objects.create(name=name, session_end_year=session_end_year, session_start_year=session_start_year)
            session.save()
            messages.success(request, 'Session Added')
            return redirect(sessions)
        except:
            messages.error(request, 'Session Failed to add')
            return redirect(sessions)
    context = {
        "sessions":all_sessions,
    }
    return render(request, "profiles/Admin Templates/manage-session.html", context)
def edit_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    if request.method == "POST":
        name = request.POST.get('name')
        session_start_year = request.POST.get('start_year')
        session_end_year = request.POST.get('end_year')
        try:
            session.session_start_year = session_start_year
            session.session_end_year = session_end_year
            session.name = name
            session.save()
            messages.success(request, "Session Edited")
            return redirect(sessions)
        except:
            messages.error(request, "Session Editing Failed")
            return redirect(sessions)
    context = {
        "session":session
    }
    return render(request, "profiles/Admin Templates/edit_session.html", context)
def delete_session(request, session_id):
    session = SessionYearModel.objects.get(id=session_id)
    session.delete()
    return redirect(sessions)

# def add_session(request):
#     return render(request, 'profiles/Admin Templates/add-session.html')
def assessment(request):
    assessment = Assessment.object.all()
    if request.method == "POST":
        name = request.POST.get("name")
        total_marks = request.POST.get("total_marks")
        try:
            create_assessment = Assessment.objects.create(name=name, total_marks=total_marks)
            create_assessment.save()
            messages.success(request, "Assessment Added")
            return redirect(assessment)
        except:
            messages.success(request, "Operation Failed")
            return redirect(assessment)
        
@login_required(login_url='login')
def student_leave_view(request):
    leaves = StudentLeave.objects.all()
    return render(request, 'profiles/Admin Templates/student-leave.html', {'leaves':leaves})

@login_required(login_url='login')
def student_leave_approve(request, leave_id):
    leave = StudentLeave.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('student_leave_view')

@login_required(login_url='login')
def student_leave_reject(request, leave_id):
    leave = StudentLeave.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='login')
def staff_leave_view(request):
    leaves = StaffLeave.objects.all()
    return render(request, 'profiles/Admin Templates/staff-leave.html', {'leaves':leaves})

@login_required(login_url='login')
def staff_leave_approve(request, leave_id):
    leave = StaffLeave.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='login')
def staff_leave_reject(request, leave_id):
    leave = StaffLeave.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')

@login_required(login_url='login')
def student_feedback_view(request):
    feedbacks = FeedBackStudent.objects.all()       
    return render(request, 'profiles/Admin Templates/student_feedback_view.html', {'feedbacks':feedbacks})

@login_required(login_url='login')
def student_feedback_message_reply(request, feedback_id):
    if request.method == "POST":
        # feedback_id = request.POST.get('id')
        feedback_reply = request.POST.get('reply')
        print(feedback_id)
        print(feedback_reply)
        feedback_obj = FeedBackStudent.objects.get(id=feedback_id)
        sender = feedback_obj.student_id.admin.first_name
        
        try:
            feedback_obj.feedback_reply = feedback_reply
            feedback_obj.save()
            messages.success(request, 'Reply sent to ' + sender)
            return redirect(student_feedback_view)
        except:
            messages.error(request, 'Reply failed to send, try again')
            return redirect(student_feedback_view)

@login_required(login_url='login')
def staff_feedback_view(request):
    feedbacks = FeedBackStaffs.objects.all()       
    return render(request, 'profiles/Admin Templates/staff_feedback_view.html', {'feedbacks':feedbacks})

@login_required(login_url='login')
def staff_feedback_message_reply(request, feedback_id):
    if request.method == "POST":
        # feedback_id = request.POST.get('id')
        feedback_reply = request.POST.get('reply')
        print(feedback_id)
        print(feedback_reply)
        feedback_obj = FeedBackStaffs.objects.get(id=feedback_id)
        sender = feedback_obj.staff_id.admin.first_name
        
        try:
            feedback_obj.feedback_reply = feedback_reply
            feedback_obj.save()
            messages.success(request, 'Reply sent to ' + sender)
            return redirect('staff_feedback_view')
        except:
            messages.error(request, 'Reply failed to send, try again')
            return redirect('staff_feedback_view')   

@login_required(login_url='login')
def admin_delete_lecture(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    lecture.delete()
    messages.success(request, "Successfully Deleted Lecture")
    return redirect('admin_lecture_view')

def admin_assignment_view(request):
    assignment = Assignment.objects.all()
    context = {
        'assignments' : assignment
    }
    return render(request, 'profiles/Admin Templates/assignments.html', context)

def admin_examination_view(request):
    examination = Examination.objects.all()
    context = {
        'examinations' : examination
    }
    return render(request, 'profiles/Admin Templates/examination.html', context)

def admin_test_view(request):
    test = Test.objects.all()
    context = {
        'tests' : test
    }
    return render(request, 'profiles/Admin Templates/tests.html', context)

def admin_lecture_view(request):
    lecture = Lecture.objects.all()
    context = {
        'lectures' : lecture
    }
    return render(request, 'profiles/Admin Templates/lecture.html', context)

def passwordchange(request, user_id):
    user=CustomUser.objects.get(id=user_id)
    print(user)
    form = SetPasswordForm(user)
    if request.method == 'POST':
        if form.is_valid:
            password = request.POST.get('new_password1')
            # user.password = password
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Changed Successfuly.')
            
            if user.user_type == 'staff':
                return redirect('manage_staff')
            elif user.user_type == 'student':
                return redirect('manage_stud')
            elif user.user_type == 'prospective':
                return redirect('admin_prospective_view')
            else:
                return redirect('admin_home')
        
    context = {
        'form' : form,
    }
    return render(request, 'profiles/Admin Templates/passwordchange.html', context)

def edit_lecture(request, lecture_id):
    lecture=Lecture.objects.get(id=lecture_id)

    form = AdminEditLectureForm()
    form.fields['subject'].initial = lecture.subject
    form.fields['form_class'].initial = lecture.form_class
    form.fields['created_by'].initial = lecture.created_by
    form.fields['lecture_text'].initial = lecture.lecture_text
    form.fields['lecture_video'].initial = lecture.lecture_video
    form.fields['lecture_ppt'].initial = lecture.lecture_ppt
    form.fields['lecture_file'].initial = lecture.lecture_file
    form.fields['heading'].initial = lecture.heading

    if request.method == 'POST':
        form = AdminEditLectureForm(request.POST, request.FILES)
        try:
            created_by = request.POST.get('created_by')
            
            staff = Staff.objects.get(id=created_by)
            text = request.POST.get('lecture_text')
            subject = request.POST.get('subject')
            heading = request.POST.get('heading')
            classs = StudentClass.objects.get(id=request.POST.get('form_class'))
            if len(request.FILES) != 0:
                lecture_file=request.FILES.get('lecture_file')
                lecture_video=request.FILES.get('lecture_video')
                lecture_ppt=request.FILES.get('lecture_ppt')
            else:
                lecture_file = lecture.lecture_file
                lecture_video = lecture.lecture_video
                lecture_ppt = lecture.lecture_ppt

            lecture.subject = Subjects.objects.get(id=subject)
            lecture.classs = classs
            lecture.created_by = staff
            lecture.lecture_file = lecture_file
            lecture.lecture_video = lecture_video
            lecture.lecture_text = text
            lecture.lecture_ppt = lecture_ppt
            lecture.save()
            messages.success(request, "Successfully Updated Lecture")
            return redirect('admin_lecture_view')
        except:
            messages.error(request, "Lecture Update Failed")
            return redirect('admin_lecture_view')
            
    return render(request, 'profiles/Admin Templates/edit_lecture.html', {'form':form})

def Events(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Added Events Successfully')
    context = {
        'form' : form,
    }
    return render(request, 'profiles/Admin Templates/events.html', context)
def manage_events(request):
    events = UpcommingEvents.objects.all()
    import datetime
    from django.utils import timezone
    for event in events:
        if event.event_date > datetime.datetime.now().date():
            idd = event.id
            eve = UpcommingEvents.objects.get(id=idd) 
            eve.event_status = "Upcoming Event"
            eve.save()
        elif event.event_date < datetime.datetime.now().date():
            idd = event.id
            eve = UpcommingEvents.objects.get(id=idd) 
            eve.event_status = "Concluded Event"
            eve.save()

        elif event.event_date == datetime.datetime.now().date():
            idd = event.id
            eve = UpcommingEvents.objects.get(id=idd) 
            eve.event_status = "Ongoing Event"
            eve.save()
        else:
            idd = event.id
            eve = UpcommingEvents.objects.get(id=idd) 
            eve.event_status = "Unknown"
            eve.save()
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Added Events Successfully')
    
    context = {
        'events' : events,
        'form':form
    }
    return render(request, 'profiles/Admin Templates/manage_events.html', context)

def edit_event(request, event_id):
    form = EditEventForm()
    events = UpcommingEvents.objects.get(id=event_id)
    
    form.fields['event_name'].initial = events.event_name
    form.fields['event_description'].initial = events.event_description
    form.fields['event_date'].initial = events.event_date
    form.fields['event_time'].initial = events.event_time
    form.fields['event_location'].initial = events.event_location
    form.fields['image_description'].initial = events.image_description
    
    if request.method == "POST":
        form = EditEventForm(request.POST, request.FILES)
        event_name = request.POST.get('event_name')
        event_description = request.POST.get('event_description')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        event_location = request.POST.get('event_location')
        if len(request.FILES) != 0:
            image_description = request.FILES.get('profile_pic')
        else:
            image_description=events.image_description


        events.event_name = event_name
        events.event_description=event_description
        events.event_date=event_date
        events.event_time=event_time
        events.event_location=event_location
        events.image_description=image_description
        events.save()
        messages.success(request, 'Event editted successful')    
        return redirect('manage_events')
    return render(request, 'profiles/Admin Templates/edit_events.html', {'form': form})

def delete_event(request, event_id):
    event = UpcommingEvents.objects.get(id=event_id)
    event.delete()
    messages.success(request, 'Successfully Deleted Event')
    return redirect('manage_events')
def profile_page(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    print(user)
    print(user.user_type)
    # print(user.staff)
    users_list = []
    student_result = []
    if user.user_type == '1':
        admin = AdminHOD.objects.get(admin=user)
        users_list.append(admin)
    elif user.user_type == 'staff':
        staff = Staff.objects.get(admin=user)
        users_list.append(staff)

    elif user.user_type == 'student':
        student = Student.objects.get(admin=user)
        users_list.append(student)
        result = StudentResult.objects.filter(student_id=student)
        # total_score = result.subject_assignment_marks + result.subject_project_marks + result.subject_1st_test_marks + result.subject_2nd_test_marks + result.subject_exam_marks
        student_result.append(result)
    context = {
        'user':user,
        'users':users_list,
        'results':student_result,
    }
    return render(request, "profiles/profile_page.html", context)
def create_cbt(request):
    all_users = CustomUser.objects.all()
    
    if request.method == "POST":
        name = request.POST.get("name")
        duration = request.POST.get("duration")
        questions = request.POST.get("questions")
        try:
            cbt = CBT.objects.create(name=name, duration=duration, questions=questions)
            cbt.save()

            for _ in range(int(questions)):
                cbt_questions = CBTQ.objects.create(cbt=cbt)
                cbt_questions.save()
            messages.success(request, "CBT Created")
            return redirect(admin_home)
        except:
            messages.error(request, "CBT Creation Failed")
            return redirect(admin_home)
    return render(request, "profiles/cbt.html")
def set_cbt(request, cbt_id):
    cbt = CBT.objects.get(id=cbt_id)
    cbt_questions = CBTQ.objects.filter(cbt=cbt)

    if request.method == "POST":
        for cbt_question in cbt_questions:
            question_id = cbt_question.id
            question = request.POST.get(f"question_{question_id}")
            options = request.POST.get(f"option_{question_id}")
            answer = request.POST.get(f"answer_{question_id}")

            try:
                cbt_question.question = question
                cbt_question.options = options
                cbt_question.answer = answer
                cbt_question.save()
            except:
                messages.error(request, 'CBT failed to set')
                return redirect(create_cbt)

        messages.success(request, 'CBT set successfully')
        return redirect(create_cbt)

    context = {
        'cbt_questions': cbt_questions
    }
    return render(request, 'profiles/setcbt.html', context)


def bulk_email(request):
    if request.method == "POST":
        send_to = request.POST.get('send_to')
        subject = request.POST.get('subject')
        get_message = request.POST.get('message')
        try:
            subject = subject
            message = get_message
            email_from = request.user.email
            if send_to == "all":
                all_users = CustomUser.objects.all()
                email_list = []
                for user in all_users:
                    emails = user.email 
                    email_list.append(emails)
                print(email_list)
                a = send_mail(subject, message, email_from, email_list)
            elif send_to == "teachers":
                teachers = CustomUser.objects.filter(user_type = 'staff')
                email_list = []
                for teacher in teachers:
                    emails = teacher.email 
                    email_list.append(emails)
                print(email_list)
                a = send_mail(subject, message, email_from, email_list)

            elif send_to == "students":
                students = CustomUser.objects.filter(user_type = 'student')
                email_list = []
                for student in students:
                    emails = student.email 
                    email_list.append(emails)
                print(email_list)
                a = send_mail(subject, message, email_from, email_list)

            elif send_to == "parents":
                print("Send to parents")
            elif send_to == "prospects":
                prospects = CustomUser.objects.filter(user_type = 'prospective')
                email_list = []
                for prospect in prospects:
                    emails = prospect.email 
                    email_list.append(emails)
                print(email_list)
                a = send_mail(subject, message, email_from, email_list)
            bulk_save = BulkEmail.objects.create(message=message, sent_to=send_to, sent_by=email_from)
            bulk_save.save()
            messages.success(request, f'Email sent successfully to {send_to}')
            return redirect(bulk_email)
        except:
            messages.error(request, 'Error sending email')
    return render(request, 'profiles/Admin Templates/bulk_email.html')