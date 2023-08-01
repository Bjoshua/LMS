from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from users.models import CustomUser
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
# from users.models import UpcommingEvents

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def offers(request):
    return render(request, 'offers.html')

def contacts(request):
    return render(request, 'contacts.html')

def events(request):
    event = UpcommingEvents.objects.all()
    context = {
       'event': event,
    }
    return render(request, 'events.html', context)
    # return render(request, 'home.html', {'post':post})

# @login_required (login_url='login')
def calendar(request):
    return render(request, 'calendar.html')

def Register(request):
    registered = False
    form = Prospective_UserForm()
    if request.method == 'POST':
        form = Prospective_UserForm(request.POST)
        if form.is_valid:
            # uuu = form.save()
            # print(uuu)
            name = request.POST.get('fullname')
            username = request.POST.get('username')
            email = request.POST.get('email')        
            phone_number = request.POST.get('phone_number')        
            user_status = request.POST.get('user_status')        
            user_type = 'prospective'
            password = request.POST.get('password1')
            if len(request.POST) != 0:
                try:
                    uuu = CustomUser.objects.create_user(
                        username = username, 
                        email=email,
                        user_type=user_type,
                        password=password
                    )
                    uuu.save()

                    candidate = Prospective_Candidate.objects.create(admin=uuu, name=name, email=email, phone_number=phone_number, user_status=user_status)
                    candidate.save()
                    try:
                        if uuu:
                            subject = 'Welcome to GVIC...'
                            message = f'Hi, {name}, Thank you for registering at GVIC, Visit the school for further registration or make a call through for more enquiry.\nAddress: No 19, Ilorin, Nigeria.\nContacts: 09025675945.'
                            email_from = settings.EMAIL_HOST_USER
                            receipient_email = [email,]
                            a = send_mail(subject, message, email_from, receipient_email)
                            
                    except:
                        print('Error sending Mail...\nInternet connection needed')
                        # return HttpResponse('Error sending Mail...\nInternet connection needed')

                except:
                    return messages.error('Error registering\nChange username and try again!!')

                use = authenticate(request, username=username, password=password)
                if use != None:
                    a = login(request, use)
                    print(a)
                    messages.success(request, f"Dear {name}, Thank you for registering. We will send you a feedback.")
                registered = True
                return redirect('home')
            else:
                messages.error(request, f"Dear {name}, Error encountered during registration, Try again.")
                return redirect('register')
        else:
            messages.error(request, f"Dear {name}, Error encountered during registration, Try again.")
            return redirect('register')
        # except:        
        #     messages.error(request, f"Dear {name}, Error encountered during registration, Try again. We will send you a feedback. ")
        #     return redirect('register')

    context = {
        'registered' : registered,
        'form' : form,
    }
    return render(request, 'register.html', context)
    
# def Register_prospects(request):
#     registered = False
#     form = Prospective_UsersForm()
#     if request.method == 'POST':
#         form = Prospective_UsersForm(request.POST)
#         if form.is_valid:
#           email = form.cleaned_data['email']
#             for userss in CustomUser.objects.all():
#                 if email == userss.email:
#                     messages.error(request, "A user with that Email address exists")
#                     return redirect('add_stud')
#                     break
#                 else:
#                     user_types = form.cleaned_data['user_type']
#                     user = form.save()
#                     first_name = form.cleaned_data['first_name']
#                     last_name = form.cleaned_data['last_name']
#                     username = form.cleaned_data['username']
#                     email = form.cleaned_data['email']      
#                     user_type = 'prospective'
#             # password = 'prospectiveuser'
#             if len(request.POST) != 0:
#                 try:
#                     uuu = CustomUser.objects.create_user(
#                         username = username, 
#                         email=email,
#                         user_type=user_type,
#                         password=password
#                     )
#                     uuu.save()

#                     candidate = Prospective_Candidate.objects.create(admin=uuu, name=name, email=email, phone_number=phone_number, user_status=user_status)
#                     candidate.save()
#                     try:
#                         if uuu:
#                             subject = 'Welcome to GVIC...'
#                             message = f'Hi, {name}, Thank you for registering at GVIC, Visit the school for further registration or make a call through for more enquiry.\nAddress: No 19, Ilorin, Nigeria.\nContacts: 09025675945.'
#                             email_from = settings.EMAIL_HOST_USER
#                             receipient_email = [email,]
#                             a = send_mail(subject, message, email_from, receipient_email)
#                             print(a)
#                     except:
#                         print('Error sending Mail...\nInternet connection needed')
#                         # return HttpResponse('Error sending Mail...\nInternet connection needed')

#                 except:
#                     return messages.error('Error registering\nChange username and try again!!')

#                 use = authenticate(request, username=username, password=password)
#                 if use != None:
#                     a = login(request, use)
#                     print(a)
#                     messages.success(request, f"Dear {name}, Thank you for registering. We will send you a feedback.")
#                 registered = True
#                 return redirect('home')
#             else:
#                 messages.error(request, f"Dear {name}, Error encountered during registration, Try again.")
#                 return redirect('register')
#         else:
#             messages.error(request, f"Dear {name}, Error encountered during registration, Try again.")
#             return redirect('register')
#         # except:        
#         #     messages.error(request, f"Dear {name}, Error encountered during registration, Try again. We will send you a feedback. ")
#         #     return redirect('register')

#                 context = {
#                     'registered' : registered,
#                     'form' : form,
#                 }
#     return render(request, 'register.html', context)
#     email = form.cleaned_data['email']
#             for userss in CustomUser.objects.all():
#                 if email == userss.email:
#                     messages.error(request, "A user with that Email address exists")
#                     return redirect('add_stud')
#                     break
#                 else:
#                     user_types = form.cleaned_data['user_type']
#                     user = form.save()
#                     first_name = form.cleaned_data['first_name']
#                     last_name = form.cleaned_data['last_name']
#                     username = form.cleaned_data['username']
#                     email = form.cleaned_data['email']
#                     print(user_types)
                    
#                     password = form.cleaned_data['password1']
#                     address = form.cleaned_data['address']
#                     session_year_id = form.cleaned_data['session_joined']
#                     phone_number = request.POST.get('parent_phone_number')
#                     # student_class = form.cleaned_data('student_class')
#                     gender = form.cleaned_data['gender']

#                     student_class = request.POST.get('student_class')
#                     parent_name = request.POST.get('parent_name')
#                     age = request.POST.get('age')
#                     date_of_birth = request.POST.get('date_of_birth')
#                     parent_status = request.POST.get('parent_status')

#                     if len(request.FILES) != 0:
#                         profile_pic = request.FILES.get('profile_pic')
#                     else:
#                         profile_pic=None
                        
#                     department_id = request.POST.get('department')
#                     print(department_id)

                                
#                     # try:
#                         # user = CustomUser.objects.create(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3, is_active=True)
#                     student_classs = StudentClass.objects.get(id=student_class)
#                     department_ids = Department.objects.get(id=department_id)
#                     session_year_ids = SessionYearModel.objects.get(id=session_year_id)

#                     student = Student.objects.create(admin=user, parent_name=parent_name, parent_status=parent_status, address= address, student_class=student_classs, department_id=department_ids, session_year_id=session_year_ids, gender=gender, parents_phone_number=phone_number, age=age, profile_pic=profile_pic, user_types='3', date_of_birth=date_of_birth)
#                     student.save()