"""Gvic_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from users import adminview, studentview, staffview
from Schoolapp import views as webview
from chat import views as chatview

urlpatterns = [
    path('django_superuser_admin_panel/', admin.site.urls, name="admin"),
    # path('', include('Schoolapp.urls'), name='schoolapp'),
    path('users/', include('users.urls'), name='users'),
    path('', webview.home, name='home'),
    path('about/', webview.about, name='about'),
    path('offers/', webview.offers, name='offers'),
    path('contacts/', webview.contacts, name='contacts'),
    path('events/', webview.events, name='events'),
    path('calendar/', webview.calendar, name='calendar'),

    path('room/<room_id>/', chatview.display_room, name="room"),
    path('room/<room_id>/', chatview.display_room, name="room"),
    path('delete_message/<room_id>/<message_id>/', chatview.delete_message, name="delete_message"),
    path('delete_message_personal/<receiver_pk>/<message_id>/', chatview.delete_message_personal, name="delete_message_personal"),
    path('edit_message/<room_id>/<message_id>/', chatview.edit_message, name="edit_message"),
    path('edit_message_personal/<receiver_pk>/<message_id>/', chatview.edit_message_personal, name="edit_message_personal"),

    path('personal_chat/<receiver_pk>/', chatview.Sendpersonalmessage, name="personal_message"),
    path('chhose_chat/', chatview.Chatroom, name="display_room"),
    # path('send_message/<room_id>/', chatview.send_message, name="send_message"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
