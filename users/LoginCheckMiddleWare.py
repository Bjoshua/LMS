from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect
from django.urls import reverse


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        # print(modulename)
        user = request.user


        if modulename == "Schoolapp.views":
            pass
        else:
            if user.is_authenticated:
                if user.user_type == "1":
                    if modulename == "users.adminview":
                        pass
                    elif modulename == "Schoolapp.views":
                        pass
                    elif modulename == "django.contrib.admin.sites":
                        pass
                    elif modulename == "users.views" or modulename == "django.views.static":
                        pass
                    else:
                        return redirect("admin_home")
                
                elif user.user_type == "staff":
                    if modulename == "users.staffview":
                        pass
                    elif modulename == "Schoolapp.views":
                        pass
                    elif modulename == "chat.views":
                        pass
                    elif modulename == "users.views" or modulename == "django.views.static":
                        pass
                    else:
                        return redirect("staff_home")
                
                elif user.user_type == "student":
                    if modulename == "users.studentview":
                        pass
                    elif modulename == "Schoolapp.views":
                        pass
                    elif modulename == "chat.views":
                        pass
                    elif modulename == "users.views" or modulename == "django.views.static":
                        pass
                    else:
                        return redirect("student_home")
                elif user.user_type == "prospective":
                    if modulename == "Schoolapp.views":
                        pass
                    elif modulename == "users.views" or modulename == "django.views.static":
                        pass

                    else:
                        return redirect("home")

                else:
                    return redirect("login")
                    # pass

            else:
                if request.path == reverse("login") or request.path == reverse("login_user") or request.path == reverse("home"):
                    pass
                else:
                    # pass
                    return redirect("login")
                
                