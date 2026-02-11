"""
URL configuration for airline_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from . import views

urlpatterns = [ 
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    path('results/<str:items>/', views.results, name='results'),
    path('book/<str:flight_id>/', views.book, name='book'),
    path('passengers/<str:booking_id>/', views.passengers, name='passengers'),

    path('manage/<str:booking_id>/', views.manage, name='manage'),
    path('experience/', views.experience, name='experience'),
    path('destination/', views.destination, name='destination'),
    path('loyalty/', views.loyalty, name='loyalty'),
    path('help/', views.help, name='help'),
    path('spline/', views.spline, name='spline'),

    path('', include('payment.urls')),  # Include payment app URLs
    
    path('admin_panel/', include('admin_panel.urls')),

    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    #  path('adminlogin/', views.adminlogin, name='adminlogin'),
#    path('adminpage/', views.adminpage, name='adminpage'),
#    path('add_flight/', views.add_flight, name='add_flight'),
    path('logout/', views.logout, name='logout'),

    #  path('add_page/', views.add_page, name='add_page'),  # Ensure this line is present
    # path('generate_flight_report/', views.generate_flight_report, name='generate_flight_report'),
    # path('generate_employee_report/', views.generate_employee_report, name='generate_employee_report'),
    # path('manage_employees/', views.manage_employees, name='manage_employees'),

    # path('adminpage/', admin_dashboard, name='admin_dashboard'),  # This is the URL for the admin dashboard
    # path('add_flight/', add_flight, name='add_flight'),
    #  path('add_flight/', add_flight, name='add_flight'),

    #  path('manage_employees/', manage_employees, name='manage_employees'),
    # path('add_employee/', add_employee, name='add_employee'),
    # path('delete_employee/<str:employee_id>/', delete_employee, name='delete_employee'),

]