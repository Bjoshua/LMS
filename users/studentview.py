from django.shortcuts import render
# from users.forms import AddStudentForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, AdminHOD, Subjects, Department, Staff, CustomUser,StudentResult, SessionYearModel, StudentClass, StaffLeave, StudentLeave, FeedBackStaffs, FeedBackStudent
from users.EmailBackEnd import EmailBackEnd
from django.http import HttpResponse
# from .forms import AddStudentForm, AddSubjectForm, AddClassForm
from .forms import *
from chat.models import *
from chat.views import display_room
def stud_room_access(request, student_id):
    student = Student.objects.get(id=student_id)
    room = Room.objects.get(members=student)
    room_id =room.id
    if room:
        return redirect(display_room, room_id)
    else:
        messages.error(request, 'Cannot Access Chat Group')
        return redirect('student_home')
@login_required(login_url='login')
def student_home_profile(request):
    student = Student.objects.get(admin=request.user)
    classs = StudentClass.objects.all()
    department = student.department_id
    department2 = Department.objects.get(id=5)
    subjects1 = Subjects.objects.filter(department_id=department)
    subjects2 = Subjects.objects.filter(department_id=department2)
    total_sub = subjects2 or subjects1
    dep_count = subjects1.count()+subjects2.count()
    print(department)
    print(department2)
    print(total_sub)
    print(dep_count)
    context = {
        'student':student,
        'class':classs,
        'dep_count':dep_count,
        'total_sub':total_sub,
    }
    return render(request, 'profiles/Student Templates/home.html', context)

    
@login_required(login_url='login')
def student_feedback(request):
    student = Student.objects.get(admin=request.user)
    feedbacks = FeedBackStudent.objects.filter(student_id=student)
    if request.method == "POST":
        student = Student.objects.get(admin=request.user)
        feedback_message = request.POST.get('feedback')
        # print(student)
        # print(leave_message)
        try:
            feedback = FeedBackStudent(student_id=student, feedback=feedback_message)
            feedback.save()
            messages.success(request, 'Leave Application sent wait for approval')
            return render(request, 'profiles/Student Templates/feedback.html',{'feedbacks':feedbacks})
        except:
            messages.error(request, 'Leave Application failed try again')
            return render(request, 'profiles/Student Templates/feedback.html',{'feedbacks':feedbacks})
    
    return render(request, 'profiles/Student Templates/feedback.html',{'feedbacks':feedbacks})     



@login_required(login_url='login')
def student_assignment(request):
    form = studentassignment()
    department1 = Department.objects.get(id=request.user.student.department_id.id)
    department2 = Department.objects.get(id=5)
    print(department2)
    assignments = Assignment.objects.filter(department_id=department1, form_class=request.user.student.student_class) or  Assignment.objects.filter(department_id=department2, form_class=request.user.student.student_class)
    # print(assignments.subject)
    if request.method == 'POST':
        form = studentassignment(request.POST, request.FILES)
        student = request.user.id
        text = request.POST.get('question_text')
        if len(request.FILES) != 0:
            question_file = request.FILES['question_file']
        else: 
            question_file = None
            
        subjects=request.POST.get('subject_id')
        # print(subjects)
        
        assignment_id=request.POST.get('assignment_id')
        assignmentsss = Assignment.objects.get(id=assignment_id)
        submit = Submitted_Assignment.objects.all()
        if len(submit) == 0:
            print("length of 0")
            assign = Submitted_Assignment.objects.create(submitted_by=request.user.student, submitted_assignment_text=text, submitted_assignment_file=question_file, subject=Subjects.objects.get(id=subjects), assignment=assignmentsss, submitted_status=True)
            assign.save()
            messages.success(request, "Successfully Submitted Assignment")
            return redirect('student_assignment')
        else:
            for assignment_submitted in submit:
                ass = Submitted_Assignment.objects.filter(submitted_by=request.user.student.id, subject=Subjects.objects.get(id=subjects), assignment=assignmentsss).exists()
                if ass:
                    messages.error(request, f'Assignment submitted already, you can\'t submit again.')
                    return redirect('student_assignment')
                    break

                else:
                    assign = Submitted_Assignment.objects.create(submitted_by=request.user.student, submitted_assignment_text=text, submitted_assignment_file=question_file, subject=Subjects.objects.get(id=subjects), assignment=assignmentsss, submitted_status=True)
                    assign.save()
                    messages.success(request, "Successfully Submitted Assignment")
                    return redirect('student_assignment')

    context = {
        'form' : form,
        'assignments' : assignments,
    }

    return render(request, 'profiles/Student Templates/assignment.html', context)


@login_required(login_url='login')
def student_test(request):
    tests = Test.objects.all()
    form = studenttest()
    if request.method == 'POST':
        form = studenttest(request.POST, request.FILES)
        student = request.user.id
        text = request.POST.get('question_text')
        if len(request.FILES) != 0:
            question_file = request.FILES['question_file']
        else: 
            question_file = None
        subject=request.POST.get('subject')

        test_id = request.POST.get('test_id')
        assignment_id = request.POST.get('assignment_id')
        particular_test = Test.objects.get(id=test_id)
        submit = Submitted_Test.objects.all()

        if len(submit) == 0:
            print("length of 0")
            assign = Submitted_Test.objects.create(submitted_by=request.user.student, submitted_test_text=text, submitted_test_file=question_file, subject=Subjects.objects.get(id=subject), test=particular_test, submitted_status=True)
            assign.save()
            messages.success(request, "Successfully Submitted Test")
            return redirect('student_test')
        else:
            for assignment_submitted in submit:
                ass = Submitted_Test.objects.filter(submitted_by=request.user.student.id, subject=Subjects.objects.get(id=subject), test=particular_test).exists()
                if ass:
                    messages.error(request, f'Test submitted already, you can\'t submit again.')
                    return redirect('student_test')
                    break
                else:
                    assign = Submitted_Test.objects.create(submitted_by=request.user.student, submitted_test_text=text, submitted_test_file=question_file, subject=Subjects.objects.get(id=subject), test=particular_test, submitted_status=True)
                    assign.save()
                    messages.success(request, "Successfully Submitted Test")
                    return redirect('student_test')
    context = {
        'form' : form,
        # 'student' : student,
        'tests' : tests,
    }

    return render(request, 'profiles/Student Templates/test.html', context)

@login_required(login_url='login')
def student_lecture(request):
    lecture = Lecture.objects.all()
    context={
        'lectures' : lecture
    }
    return render(request, 'profiles/Student Templates/lecture.html', context)

@login_required(login_url='login')
def student_examination(request):
    form = studentexam()
    examination = Examination.objects.all()    
    if request.method == 'POST':
        form = studentexam(request.POST, request.FILES)
        
        student = request.user.id
        text = request.POST.get('question_text')
        if len(request.FILES) != 0:
            question_file = request.FILES['question_file']
        else: 
            question_file = None
        subject=request.POST.get('subject')
        exam_id=request.POST.get('exam_id')
        particular_exam = Examination.objects.get(id=exam_id)
        submit = Submitted_Examination.objects.all()
        
        
        if len(submit) == 0:
            print("length of 0")
            assign = Submitted_Examination.objects.create(submitted_by=request.user.student, submitted_exam_text=text, submitted_exam_file=question_file, subject=Subjects.objects.get(id=subject), exam=particular_exam, submitted_status=True)
            assign.save()
            messages.success(request, "Successfully Submitted Examination")
            return redirect('student_examination')
        else:
            for assignment_submitted in submit:
                ass = Submitted_Examination.objects.filter(submitted_by=request.user.student.id, subject=Subjects.objects.get(id=subject), exam=particular_exam).exists()
                if ass:
                    messages.error(request, f'Examination submitted already, you can\'t submit again.')
                    return redirect('student_examination')
                    break
                else:
                    assign = Submitted_Examination.objects.create(submitted_by=request.user.student, submitted_exam_text=text, submitted_exam_file=question_file, subject=Subjects.objects.get(id=subject), exam=particular_exam, submitted_status=True)
                    assign.save()
                    messages.success(request, "Successfully Submitted Examination")
                    return redirect('student_examination')



        
        assign = Submitted_Examination.objects.create(submitted_by=request.user.student, submitted_exam_text=text, submitted_exam_file=question_file, subject=Subjects.objects.get(id=subject), exam=Subjects.objects.get(id=exam_id), submitted_status=True)
        assign.save()
        messages.success(request, "Successfully Submitted Examination")
        
        
    context = {
        'form' : form,
        'examination' : examination,
    }

    return render(request, 'profiles/Student Templates/exam.html', context)


@login_required(login_url='login')
def student_update_profile(request):
    # form = StudentUpdateProfileForm()
    customuser = CustomUser.objects.get(id=request.user.id)        
    student = Student.objects.get(admin=customuser.id)
    
    # form.fields['address'].initial = student.address
    # form.fields['parents_phone_number'].initial = student.parents_phone_number
    # form.fields['parent_name'].initial = student.parent_name
    # form.fields['parent_status'].initial = student.parent_status

    if request.method == 'POST':   
        try:
            # form = StudentUpdateProfileForm(request.POST, request.FILES)
            # age = request.POST.get('age')
            # date_of_birth = request.POST.get('date_of_birth')
            # address = request.POST.get('address')
            # parent_phone_number = request.POST.get('parents_phone_number')
            # parent_name = request.POST.get('parent_name')
            # parent_status = request.POST.get('parent_status')
            if len(request.FILES) != 0:
                profile_pic = request.FILES.get('profile_pic')
            else:
                profile_pic=student.profile_pic

            # profile_pic = request.FILES.get('profile_pic')

            # student.age = age
            # student.address = address
            # student.parents_phone_number = parent_phone_number
            # student.parent_name = parent_name
            # student.parent_status = parent_status
            student.profile_pic = profile_pic
            # student.date_of_birth = date_of_birth
            student.save()
                
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_update_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_update_profile')
    return render(request, 'profiles/Student Templates/student_update_profile.html')
    
@login_required(login_url='login')
def student_result(request):
    return render(request, 'profiles/Student Templates/results.html')

@login_required(login_url='login')
def student_leave(request):
    user = request.user
    student = user.student
    leaves = StudentLeave.objects.filter(student_id=student)
    if request.method == "POST":
        # student = Student.objects.get(admin=request.user)
        leave_message = request.POST.get('leave_message')
        print(student)
        print(leave_message)
        try:
            leave_apply = StudentLeave.objects.create(student_id=student, leave_message=leave_message, leave_status = 0)
            leave_apply.save()
            messages.success(request, 'Leave Application sent wait for approval')
            return render(request, 'profiles/Student Templates/leave.html',{'leaves':leaves})
        except:
            messages.error(request, 'Leave Application failed try again')
            return render(request, 'profiles/Student Templates/leave.html',{'leaves':leaves})
    
            
    return render(request, 'profiles/Student Templates/leave.html',{'leaves':leaves})

def assignment_view(request):
    submit = Submitted_Assignment.objects.all()
    context = {'submit':submit}
    return render(request, 'profiles/Student Templates/assignment_view.html', context)

def test_view(request):
    submit = Submitted_Test.objects.all()
    context = {'submit':submit}
    return render(request, 'profiles/Student Templates/test_view.html', context)

def exam_view(request):
    submit = Submitted_Examination.objects.all()
    context = {'submit':submit}
    return render(request, 'profiles/Student Templates/exam_view.html', context)

def subjects(request):
    subject = Subjects.objects.all()
    context = {
        'subjects' : subject
    }
    
    return render(request, 'profiles/Student Templates/subjects.html', context)
def allcbts(request): 
    student = Student.objects.get(admin=request.user)
    cbts = CBT.objects.filter(studentclass=student.student_class)
    for cbt in cbts:
        check_cbtr = CBTR.objects.filter(cbt=cbt).exists()
        if check_cbtr:
            cbtr = CBTR.objects.filter(cbt=cbt)
        else:
            cbtr = None
            # cbt.append(cbtr)
            # print(cbtr)
    context = {
        'cbts':cbts,
        'cbtr':cbtr,
    }
    return render(request, 'profiles/CBT Templates/allcbt.html', context)
def take_cbt(request, cbt_id):
    cbt = CBT.objects.get(id=cbt_id)
    cbtqs = CBTQ.objects.filter(cbt=cbt)
    student = Student.objects.get(admin=request.user)
    benchmark = int(cbt.marks)/int(cbt.questions)
    # print(benchmark)
    if request.method == "POST":
        marks = 0
        for question in cbtqs:
            try:
                answer = request.POST.get(f'answer_{question.id}')
                print(answer)
                if question.answers == answer:
                    marks = marks + benchmark
                    print(marks)
            except:
                messages.error(request, 'Operation Failed')
                return redirect(take_cbt, cbt_id)
        cbtr = CBTR.objects.create(cbt=cbt, student=student, score=marks)
        cbtr.save()
        messages.success(request, 'Your Score is ready')
        return redirect(view_score, cbtr_id=cbtr.id)
    context = {
        'cbtqs':cbtqs,
        'cbt':cbt,
    }
    return render(request, 'profiles/CBT Templates/take_cbt.html', context)
def view_score(request, cbtr_id):
    cbtr = CBTR.objects.get(id=cbtr_id)
    overall_score = cbtr.cbt.marks
    score =  cbtr.score
    total_questions = cbtr.cbt.questions
    q_got = (int(score)/int(overall_score))*int(total_questions)
    q_missed = int(total_questions)-int(q_got)
    percentage = (int(score)/int(overall_score))*100
    context = {
        'cbtr':cbtr,
        'overall_score':overall_score,
        'score':score,
        'total_questions':total_questions,
        'q_got':q_got,
        'q_missed':q_missed,
        'percentage':percentage,
    }
    return render(request, 'profiles/CBT Templates/viewscore.html', context)
