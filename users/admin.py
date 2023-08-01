from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import Student, Department,AdminHOD, Subjects, Staff, CustomUser,StudentResult, SessionYearModel, StudentClass, StaffLeave, StudentLeave, FeedBackStaffs, FeedBackStudent
from .models import *
# from .models import Teacher
# Register your models here.
class UserModel(UserAdmin):
    pass
admin.site.register(CustomUser, UserModel)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Subjects)
# admin.site.register(Staff)
admin.site.register(AdminHOD)
admin.site.register(StudentClass)
admin.site.register(SessionYearModel)
admin.site.register(StudentResult)
admin.site.register(StudentLeave)
admin.site.register(FeedBackStudent)
admin.site.register(StaffLeave)
admin.site.register(FeedBackStaffs)
admin.site.register(Department)
admin.site.register(Assignment)
admin.site.register(Test)
admin.site.register(Examination)
admin.site.register(Submitted_Assignment)
admin.site.register(Lecture)
admin.site.register(Submitted_Examination)
admin.site.register(Submitted_Test)
admin.site.register(CBT)
admin.site.register(CBTQ)
admin.site.register(CBTR)