from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Student, AdminHOD, Subjects, Department, Staff, CustomUser,StudentResult, SessionYearModel, StudentClass, StaffLeave, StudentLeave, FeedBackStaffs, FeedBackStudent
from users.EmailBackEnd import EmailBackEnd
from django.http import HttpResponse
from .forms import *
from users.studentview import stud_room_access
from users.staffview import room_access
# from Schoolapp.views import home
def group_chat_middleware(request):
    user = request.user
    if user.is_authenticated:
        if user.user_type == 'staff':
            return redirect(room_access, staff_id=request.user.staff.id)
        elif user.user_type == 'student':
            return redirect(stud_room_access, student_id=request.user.student.id)
        else:
            # messages.error(request, 'Only Staff and Students have Access to this feature')
            return HttpResponse('<h1>Only Staff and Students have Access to this feature<h1/>')
    else:
        return redirect(request, login)
# def
def student_login(request):
    return render(request, "login.html")

def Login_user(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == '1':
                return redirect('admin_home')
            
            elif user.user_type == 'staff':
                # user.staff.user_type == '2':
                    return redirect('staff_home')
            elif user.user_type == 'student':
            # if user.student.user_types == '3':
                return redirect('student_home')
            elif user.user_type == 'prospective':
            # if user.student.user_types == '3':
                return redirect('home')

            else:
                messages.error(request, "Invalid Login!")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Credentials!")
            #return HttpResponseRedirect("/")
            return redirect('login')

def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('home')

def dashboard(request):
    user=request.user
    if user != None:
        if user.user_type == '1':
            return redirect('admin_home')
        elif user.user_type == 'staff':
            return redirect('staff_home')
        elif user.user_type == 'student':
            return redirect('student_home')
        else:
            messages.error(request, "Invalid Login!")
            return redirect('login')
    else:
        messages.error(request, "Invalid Login Credentials!")
        #return HttpResponseRedirect("/")
        return redirect('login')
