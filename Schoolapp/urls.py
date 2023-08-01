from django.urls import path
from . import views
# from django.contrib.stacticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('offers/', views.offers, name='offers'),
    path('contacts/', views.contacts, name='contacts'),
    path('events/', views.events, name='events'),
    path('calendar/', views.calendar, name='calendar'),
    # path('login/', views.login, name='login'),
]
# urlpatterns =+ staticfiles_urlpatterns()