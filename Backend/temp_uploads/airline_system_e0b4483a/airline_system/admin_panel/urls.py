from django.urls import path
from . import views

urlpatterns = [
    path('adminregister/', views.adminregister, name='adminregister'),
    path('', views.adminlogin, name='adminlogin'),
    path('logout/', views.logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),

    
    # path('employee_dashboard/', views.employee_dashboard, name='employee_dashboard'),

    # Admin functionalities
    path('manage_employees/', views.manage_employees, name='manage_employees'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('add_flight/', views.add_flight, name='add_flight'),
    path('flights_report/', views.flights_report, name='flights_report'),
    path('update_employee/<str:employee_id>/', views.update_employee, name='update_employee'),
    path('update_flight/<str:flight_id>/', views.update_flight, name='update_flight'),
    path('remove_employee/<str:employee_id>/', views.remove_employee, name='remove_employee'),
    path('remove_flight/<str:flight_id>/', views.remove_flight, name='remove_flight'),
    path('download_flight_report/', views.download_flight_report, name='download_flight_report'),
    # path('update_booking/<str:booking_id>/', views.update_booking, name='update_booking'),
    # path('remove_booking/<str:booking_id>/', views.remove_booking, name='remove_booking'),

    # Employee functionalities
    # path('update_task/<str:task_id>/', views.update_task, name='update_task'),
    # path('remove_task/<str:task_id>/', views.remove_task, name='remove_task'),

    path('streamlit/', views.streamlit_app, name='streamlit_app'),

]
