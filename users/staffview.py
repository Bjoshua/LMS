from django.shortcuts import render
# from users.forms import AddStudentForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from chat.models import *
from users.EmailBackEnd import EmailBackEnd
from django.http import HttpResponse
# from .forms import AddStudentForm, AddSubjectForm, AddClassForm
from .forms import *
from chat.views import display_room

def room_access(request, staff_id):
    staff = Staff.objects.get(id=staff_id)
    room = Room.objects.get(admin=staff)
    room_id =room.id
    if room:
        return redirect(display_room, room_id)
    else:
        messages.error(request, 'Cannot Access Chat Group')
        return redirect('staff_home')
@login_required(login_url='login')
def staff_manage_class(request):
    subjects = Subjects.objects.all()
    # tests = Submitted_Test.objects.all()
    staff_class= StudentClass.objects.get(staff_id=request.user)
    students = Student.objects.filter(student_class=staff_class)
    # for student in students:
        
    tests = Test.objects.filter(form_class=staff_class)
    submitted_tests = Submitted_Test.objects.all()
    exams = Submitted_Examination.objects.all()
    
    try:
        # aaa=CustomUser.objects.filter(user_type='2')
        sub_tests = Submitted_Test.objects.all()
        sub_test_list = []
        for test in sub_tests:
            format = (test.id, test.test_name)
            sub_test_list.append(format)        
    except: 
        sub_test_list = []

    
    context = {
        'subjects' : subjects,
        'sub_tests' : submitted_tests,
        'get_test': tests,
        'students' : students,
        'exams' : exams,
    }
    return render(request, 'profiles/Staff Templates/manage_class.html', context)

@login_required(login_url='login')
def staff_home(request):
    no_student = Student.objects.count()
    teacher = Staff.objects.get(admin=request.user)
    print(teacher)
    get_class = StudentClass.objects.filter(staff_id=request.user).exists()

    # count = Student.objects.filter(student_class=request.user.staff.form_class.id)
    count = Student.objects.filter(student_class=get_class)
    assignments = Assignment.objects.filter(form_class=get_class)
    print(assignments.count())
    submitted_assignments = []
    for assignment in assignments:
        print(assignment)
        submitted = Submitted_Assignment.objects.filter(assignment=assignment)
        print(submitted)
        submitted_assignments.append(submitted)
    # Do same for Test and Exam
    print(submitted_assignments.count)

    context={
        'no_student' : no_student,
        'student_count' : count,
        'submitted_assignments': submitted_assignments,
    }
    if get_class:
        return render(request, 'profiles/Staff Templates/home.html', context)
    else:
        return render(request, 'profiles/Staff Templates/home.html', context)

@login_required(login_url='login')
def staff_manage_stud(request):
    staff_class= StudentClass.objects.get(staff_id=request.user)
    students = Student.objects.filter(student_class=staff_class)
    print(staff_class)
    print(students)
    context = {
        'students' : students,
    }
    return render(request,'profiles/staff Templates/manage-stud.html', context)

@login_required(login_url='login')
def staff_add_assignment(request):
    form = AddAssignment()
    
    if request.method == 'POST':
        form = AddAssignment(request.POST, request.FILES)
        
        teacher = request.user.id
        text = request.POST.get('question_text')
        if len(request.FILES) != 0:
            question_file = request.FILES['question_file']
        else:
            question_file = None


        subject=request.POST.get('subject')
        department=request.POST.get('department_id')
        class_id = request.POST.get('student_class') 
        
        assign = Assignment.objects.create(created_by=request.user.staff, question_text=text, question_file=question_file, subject=Subjects.objects.get(id=subject), department_id=Department.objects.get(id=department), form_class=StudentClass.objects.get(id=class_id))
        assign.save()
        messages.success(request, "Successfully Added Assignment")
        
        
    context = {
        'form' : form,
    }

    return render(request, 'profiles/Staff Templates/add_assignment.html', context)

@login_required(login_url='login')
def staff_add_test(request):
    form = AddTest()
    
    if request.method == 'POST':
        form = AddTest(request.POST, request.FILES)
        
        teacher = request.user.id
        text = request.POST.get('question_text')
        test = request.POST.get('test_name')
        subject=request.POST.get('subject')
        student_class=request.POST.get('student_class')
        if len(request.FILES) != 0:
            question_file = request.FILES.get('question_file')
        else:
            question_file = None

        
        assign = Test.objects.create(created_by=request.user.staff,form_class=StudentClass.objects.get(id=student_class), test_name=test, test_text=text, test_file=question_file,subject=Subjects.objects.get(id=subject))
        assign.save()
        messages.success(request, "Successfully Added Test")
        
    context = {
        'form' : form,
    }

    return render(request, 'profiles/Staff Templates/add_test.html', context)

@login_required(login_url='login')
def staff_add_exam(request):
    form = AddExamination()
    if request.method == 'POST':
        form = AddExamination(request.POST, request.FILES)
        teacher = request.user.id
        if len(request.FILES) != 0:
            question_file = request.FILES['question_file']
        else:
            question_file = None
        text = request.POST.get('question_text')
        subject=request.POST.get('subject')
        classs = request.POST.get('student_class')
        
        assign = Examination.objects.create(created_by=request.user.staff, form_class=StudentClass.objects.get(id=classs),examination_text=text, examination_file=question_file, subject=Subjects.objects.get(id=subject))
        assign.save()
        messages.success(request, "Successfully Added Examination")
        
    context = {
        'form' : form,
    }

    return render(request, 'profiles/Staff Templates/add_exam.html', context)

@login_required(login_url='login')
def staff_add_lectures(request):
    form = AddLecture()    
    if request.method == 'POST':
        form = AddLecture(request.POST, request.FILES)
        
        teacher = request.user.id
        text = request.POST.get('lecture_text')
        classs = request.POST.get('student_class')
        if len(request.FILES) != 0:
            lecture_file=request.FILES.get('lecture_file')
            lecture_video=request.FILES.get('lecture_video')
            lecture_ppt=request.FILES.get('lecture_ppt')
        else:
            lecture_file = None
            lecture_video = None
            lecture_ppt = None

        # lecture_file=request.FILES['lecture_file']
        # lecture_video=request.FILES['lecture_video']
        # lecture_ppt=request.FILES['lecture_ppt']
        subject=request.POST.get('subject')
        
        assign = Lecture.objects.create(created_by=request.user.staff, form_class=StudentClass.objects.get(id=classs), lecture_text=text, subject=Subjects.objects.get(id=subject),lecture_ppt=lecture_ppt, lecture_file=lecture_file, lecture_video=lecture_video)
        assign.save()
        messages.success(request, "Successfully Added Lecture")
        
    context = {
        'form' : form,
    }

    return render(request, 'profiles/Staff Templates/add_lecture.html', context)

@login_required(login_url='login')
def staff_assignment_view(request):
    staff_class = StudentClass.objects.get(staff_id=request.user)
    
    students = Student.objects.filter(student_class=staff_class)
    # print(request.user.staff)
    assignments = Assignment.objects.filter(created_by=request.user.staff)
    # print(assignments.submitted_by)
    for student in students:
        submit = Submitted_Assignment.objects.all()
        context = {
                'submit' : submit,
                'student': student,
            }
    # Submitted_Assignment.objects.filter(submitted_by = students, assignment=assignments) or Submitted_Assignment.objects.filter(submitted_by = students, assignment=assignments)
    if request.method == 'POST':
        subject=request.POST.get("subject")
        id=request.POST.get("id")
        submitted_by=request.POST.get("submitted_by")
        submitted_assignment_text=request.POST.get("submitted_assignment_text")
        scores=request.POST.get("score")

        if len(request.FILES) != 0:
            submitted_assignment_file = request.FILES['submitted_assignment_file']
        else:
            submitted_assignment_file=None
        
        submit_assignment = Submitted_Assignment.objects.get(id=id)        
        
        submit_assignment.subject = Subjects.objects.get(id=subject)
        submit_assignment.submitted_by = Student.objects.get(id=submitted_by)
        submit_assignment.submitted_assignment_text = submitted_assignment_text
        submit_assignment.submitted_assignment_file = submitted_assignment_text
        submit_assignment.assessed_by = request.user.staff
        submit_assignment.score = scores
        submit_assignment.submitted_assignment_file = submitted_assignment_file
        submit_assignment.save()
        messages.info(request, "Successfully Marked ")
    
    
    
    return render(request, 'profiles/Staff Templates/view_submitted_assignment.html', context)

@login_required(login_url='login')
def staff_exam_view(request):
    submit = Submitted_Examination.objects.all()
    if request.method == 'POST':
        id=request.POST.get("id")
        subject=request.POST.get("subject")
        submitted_by=request.POST.get("submitted_by")
        submitted_assignment_text=request.POST.get("submitted_assignment_text")
        scores=request.POST.get("score")

        if len(request.FILES) != 0:
            submitted_assignment_file = request.FILES['submitted_assignment_file']
        else: 
            submitted_assignment_file=None
        
        submit_assignment = Submitted_Examination.objects.get(id=id) 
        
        student = Student.objects.get(id=submitted_by)
        
        submit_assignment.subject = Subjects.objects.get(id=subject)
        submit_assignment.submitted_by = student
        submit_assignment.submitted_exam_text = submitted_assignment_text
        submit_assignment.assessed_by = request.user.staff
        submit_assignment.score = scores
        submit_assignment.submitted_exam_file = submitted_assignment_file
        submit_assignment.save()
        
        # StudentResult.objects.create(
        #     id=user.username+'_'+user.last_name+'_'+student.student_class,
        #     student_id=student,
        #     subject_id=Subjects.objects.get(id=subject),
        #     subject_assignment_marks = scores
        # )       
        
        messages.info(request, "Successfully Marked ")
        
    
    context = {
        'submit' : submit,
    }
    
    return render(request, 'profiles/Staff Templates/view_submitted_exam.html', context)

@login_required(login_url='login')
def staff_marked_assignment_view(request):
    submit = Submitted_Assignment.objects.all()
    context = {
        'submit' : submit,
    }

    return render(request, 'profiles/Staff Templates/marked_assignment.html', context)

@login_required(login_url='login')
def staff_marked_test_view(request):
    submit = Submitted_Test.objects.all()
    context = {
        'submit' : submit,
    }
    return render(request, 'profiles/Staff Templates/marked_test.html', context)

@login_required(login_url='login')
def staff_marked_examination_view(request):
    submit = Submitted_Examination.objects.all()
    context = {
        'submit' : submit,
    }
    return render(request, 'profiles/Staff Templates/marked_exam.html', context)
    
@login_required(login_url='login')
def staff_test_view(request):
    submit = Submitted_Test.objects.all()
    if request.method == 'POST':
        id=request.POST.get("id")
        subject=request.POST.get("subject")
        submitted_by=request.POST.get("submitted_by")
        submitted_assignment_text=request.POST.get("submitted_assignment_text")
        scores=request.POST.get("score")
        if len(request.FILES) != 0:
            submitted_assignment_file = request.FILES['submitted_assignment_file']
        else: 
            submitted_assignment_file=None        
        
        submit_assignment = Submitted_Test.objects.get(id=id)        

        student = Student.objects.get(id=submitted_by)
        
        submit_assignment.subject = Subjects.objects.get(id=subject)
        submit_assignment.submitted_by = student
        submit_assignment.submitted_test_text = submitted_assignment_text
        submit_assignment.submitted_file_text = submitted_assignment_text
        submit_assignment.assessed_by = request.user.staff
        submit_assignment.score = scores
        submit_assignment.submitted_assignment_file = submitted_assignment_file
        submit_assignment.save()
        messages.info(request, "Successfully Marked ")        
    
    context = {
        'submit' : submit,
    }
    
    return render(request, 'profiles/Staff Templates/view_submitted_test.html', context)
    
@login_required(login_url='login')
def staff_record_assessment(request):
    pass
    

@login_required(login_url='login')
def staff_leave(request):
    user = request.user
    staff = user.staff
    leaves = StaffLeave.objects.filter(staff_id=staff)
    if request.method == "POST":
        # student = Student.objects.get(admin=request.user)
        leave_message = request.POST.get('leave_message')
        print(staff)
        print(leave_message)
        try:
            leave_apply = StaffLeave.objects.create(staff_id=staff, leave_message=leave_message, leave_status = 0)
            leave_apply.save()
            messages.success(request, 'Leave Application sent wait for approval')
            return render(request, 'profiles/Staff Templates/leave.html',{'leaves':leaves})
        except:
            messages.error(request, 'Leave Application failed try again')
            return render(request, 'profiles/Staff Templates/leave.html',{'leaves':leaves})
    
            
    return render(request, 'profiles/Staff Templates/leave.html',{'leaves':leaves})

@login_required(login_url='login')
def staff_feedback(request):
    user=request.user
    staff = user.staff
    feedbacks = FeedBackStaffs.objects.filter(staff_id=staff)
    if request.method == "POST":
        # student = Student.objects.get(admin=request.user)
        feedback_message = request.POST.get('feedback')
        # print(student)
        # print(leave_message)
        try:
            feedback = FeedBackStaffs(staff_id=staff, feedback=feedback_message)
            feedback.save()
            messages.success(request, 'Leave Application sent wait for approval')
            return redirect('staff_feedback')
        except:
            messages.error(request, 'Leave Application failed try again')
            return redirect('staff_feedback')    
            
    return render(request, 'profiles/Staff Templates/feedback.html',{'feedbacks':feedbacks})

@login_required(login_url='login')
def staff_update_profile(request):
    # address, form_class, profile_pic, phone_number
    form = StaffUpdateProfileForm()
    customuser = CustomUser.objects.get(id=request.user.id)        
    staff = Staff.objects.get(admin=customuser.id)

    form.fields['address'].initial = staff.address
    form.fields['phone_number'].initial = staff.phone_number

    if request.method == 'POST':   
        # try:
        form = StaffUpdateProfileForm(request.POST, request.FILES)
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        
        if len(request.FILES) != 0:
            profile_pic = request.FILES.get('profile_pic')
        else:
            profile_pic = staff.profile_pic

        staff.address = address
        staff.phone_number = phone_number
        staff.profile_pic = profile_pic
        staff.save()
        messages.success(request, "Profile Updated Successfully")
        return redirect('staff_update_profile')

        # except:
                # messages.success(request, "Profile Updated Successfully")
                # return redirect('staff_update_profile')
        
    return render(request, 'profiles/Staff Templates/staff_update_profile.html', {'form':form})

@login_required(login_url='login')
def delete_lecture(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    lecture.delete()
    messages.success(request, "Successfully Deleted Lecture")
    return redirect('staff_lecture_view')

@login_required(login_url='login')
def staff_lecture_view(request):
    lecture = Lecture.objects.all()
    context={
        'lectures' : lecture
    }
    return render(request, 'profiles/Staff Templates/lecture.html', context)


def edit_lecture(request, lecture_id):
    lecture=Lecture.objects.get(id=lecture_id)

    form = StaffEditLectureForm()
    form.fields['subject'].initial = lecture.subject
    form.fields['form_class'].initial = lecture.form_class
    form.fields['lecture_text'].initial = lecture.lecture_text
    form.fields['lecture_video'].initial = lecture.lecture_video
    form.fields['lecture_ppt'].initial = lecture.lecture_ppt
    form.fields['lecture_file'].initial = lecture.lecture_file
    form.fields['heading'].initial = lecture.heading

    if request.method == 'POST':
        form = StaffEditLectureForm(request.POST, request.FILES)
        try:
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
            lecture.created_by = request.user.staff
            lecture.lecture_file = lecture_file
            lecture.lecture_video = lecture_video
            lecture.lecture_text = text
            lecture.lecture_ppt = lecture_ppt
            lecture.save()
            messages.success(request, "Successfully Updated Lecture")
            return redirect('staff_lecture_view')
        except:
            messages.error(request, "Lecture Update Failed")
            return redirect('staff_lecture_view')
            
    return render(request, 'profiles/Admin Templates/edit_lecture.html', {'form':form})
@login_required(login_url='login')
def create_cbt(request):
    all_users = CustomUser.objects.all()
    form = CreateCbtForm()
    staff_class = StudentClass.objects.get(staff_id=request.user)
    cbts = CBT.objects.filter(studentclass=staff_class)
    if request.method == "POST":
        form = CreateCbtForm(request.POST)
        name = request.POST.get("name")
        duration = request.POST.get("duration")
        questions = request.POST.get("questions")
        marks = request.POST.get("marks")
        get_subject = request.POST.get("subject")
        get_classs = request.POST.get("classs")
        subject = Subjects.objects.get(id=get_subject)
        classs = StudentClass.objects.get(id=get_classs)
        try:
            cbt = CBT.objects.create(name=name, duration=duration, questions=questions, studentclass=classs, subject=subject, marks=marks)
            cbt.save()

            for _ in range(int(questions)):
                cbt_questions = CBTQ.objects.create(cbt=cbt)
                cbt_questions.save()
            messages.success(request, "CBT Created")
            return redirect(set_cbt, cbt_id=cbt.id)
        except:
            messages.error(request, "CBT Creation Failed")
            return redirect(create_cbt)
    context = {
        'form':form,
        'cbts':cbts
    }
    return render(request, "profiles/CBT Templates/cbt.html", context)
def set_cbt(request, cbt_id):
    cbt = CBT.objects.get(id=cbt_id)
    cbt_questions = CBTQ.objects.filter(cbt=cbt)
    form = QuestionForm()
    if request.method == "POST":
        for cbt_question in cbt_questions:
            question_id = cbt_question.id
            question = request.POST.get(f"question_{question_id}")
            option1 = request.POST.get(f"option1_{question_id}")
            option2 = request.POST.get(f"option2_{question_id}")
            option3 = request.POST.get(f"option3_{question_id}")
            option4 = request.POST.get(f"option4_{question_id}")
            answer = request.POST.get(f"answer_{question_id}")
            print(question)
            print(option1)
            print(option2)
            print(option3)
            print(option4)
            print(answer)
            try:
                cbt_question.question = question
                cbt_question.option1 = option1
                cbt_question.option2 = option2
                cbt_question.option3 = option3
                cbt_question.option4 = option4
                cbt_question.answers = answer
                cbt_question.save()
            except:
                messages.error(request, 'CBT failed to set')
                return redirect(create_cbt)
        messages.success(request, 'CBT Questions set successfully')
        return redirect(create_cbt)
        

    context = {
        'cbt_questions': cbt_questions,
        'form':form
    }
    return render(request, 'profiles/CBT Templates/setcbt.html', context)
