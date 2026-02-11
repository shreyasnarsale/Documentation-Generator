# Create your views here.

from django.shortcuts import render, redirect
from bson.objectid import ObjectId

import bcrypt # type: ignore
from django.shortcuts import render, redirect
from pymongo import MongoClient
from django.http import HttpResponseForbidden, HttpResponse
from functools import wraps
from django.contrib import messages
from datetime import datetime
# MongoDB connection
client = MongoClient("mongodb+srv://youtubepy:youtubepy@cluster0.hlekbr4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client['airline_reservation_system']

def adminregister(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']  # Either 'Admin' or 'Employee'

        # Hash password
        # hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert into MongoDB
        db.users.insert_one({
            "email": email,
            "password": password,
            "role": role
        })

        messages.success(request, "Registration successful!")
        return redirect('adminlogin')

    return render(request, 'adminregister.html')

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Fetch user from MongoDB
        user = db.users.find_one({"email": email})
        if user and password== user['password']:
            # Set session
            # request.session['user_email'] = email
            # request.session['role'] = user['role']
            
            if user['role'] == 'Admin':
                return redirect('admin_dashboard')
            else:
                return redirect('employee_dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('adminlogin')

    return render(request, 'adminlogin.html')
def logout(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('adminlogin')



# Helper function for role-based access control
def role_required(role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = db.users.find_one({"email": request.session.get('user_email')})
            if user and user['role'] == role:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You are not authorized to view this page")
        return _wrapped_view
    return decorator

# View for Admin Dashboard
# @role_required('Admin')
def admin_dashboard(request):
    # Fetch all employees and bookings
    employees = db.users.find({"role": "Employee"})
    bookings = db.bookings.find()

    context = {
        'employees': employees,
        'bookings': bookings
    }
    return render(request, 'admin_dashboard.html', context)

def manage_employees(request):
    # Fetch all employees and bookings
    employees = list(db.users.find({"role": "Employee"}))
    
    for employee in employees:
        employee['id']=str( employee['_id'])
    context = {
        'employees': employees
    }

    return render(request, 'manage_employees.html', context)
def flights_report(request):

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if start_date_str and end_date_str:
            # Convert strings to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Query flights within the date range
            flights = db.flights.find({
                'departure_time': {
                    '$gte': start_date,
                    '$lt': end_date.replace(hour=23, minute=59, second=59)
                }
            })

            flights_list = list(flights)  # Convert cursor to a list

            # Render the report with flight data
            return render(request, 'flights_report.html', {'flights': flights_list, 'start_date': start_date, 'end_date': end_date})


    # Fetch all flights
    flights = list(db.flights.find({}))
    total_flights = len(flights)
    for flight in flights:
        flight['id']=str( flight['_id'])
    context = {
        'flights': flights,
        'total_flights': total_flights
    }

    return render(request, 'flights_report.html', context)

# Add new Employee
def add_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        db.users.insert_one({"name": name, "email": email, "password": password, "role": "Employee"})
        return redirect('manage_employees')
    return HttpResponse('add_employee.html')
def add_flight(request):
    if request.method == 'POST':
        flight_number = request.POST['flight_number']
        departure_city = request.POST['departure_city']
        arrival_city = request.POST['arrival_city']

        arrival_time = datetime.strptime(request.POST['arrival_time'] , "%Y-%m-%dT%H:%M")
        departure_time =datetime.strptime(request.POST['departure_time'] , "%Y-%m-%dT%H:%M")
        price = int(request.POST['price'])
        total_seats =int(request.POST['total_seats'])


        db.flights.insert_one({"flight_number": flight_number, "departure_city": departure_city, "arrival_city" :arrival_city, "arrival_time": arrival_time, "departure_time": departure_time, "price": price, "total_seats": total_seats})
        return redirect('admin_dashboard')
    return render(request,'add_flight.html')

# Update Employee Details
def update_employee(request, employee_id):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        db.users.update_one({'_id': ObjectId(employee_id)}, {"$set": {'name': name, "email": email, "password": password}})
        return redirect('manage_employees')
    
    employee = db.users.find_one({'_id': ObjectId(employee_id)})
    employee['id']=str( employee['_id'])
    return render(request, 'update_employee.html', {'employee': employee})
# Update Flight Details
def update_flight(request, flight_id):
    if request.method == 'POST':
        
        flight_number = request.POST['flight_number']
        departure_city = request.POST['departure_city']
        arrival_city = request.POST['arrival_city']

        arrival_time = datetime.strptime(request.POST['arrival_time'] , "%Y-%m-%dT%H:%M")
        departure_time =datetime.strptime(request.POST['departure_time'] , "%Y-%m-%dT%H:%M")
        price = int(request.POST['price'])
        total_seats =int(request.POST['total_seats'])


        db.flights.update_one({'_id': ObjectId(flight_id)},{"$set": {"flight_number": flight_number, "departure_city": departure_city, "arrival_city" :arrival_city, "arrival_time": arrival_time, "departure_time": departure_time, "price": price, "total_seats": total_seats}})
        return redirect('flights_report')
    flight= db.flights.find_one({'_id': ObjectId(flight_id)})
    flight['id']=str(flight['_id'])
    return render(request, 'update_flight.html', {'flight': flight } )
    

     

# Remove Employee
def remove_employee(request, employee_id):
    db.users.delete_one({'_id': ObjectId(employee_id)})
    return redirect('manage_employees')
def remove_flight(request, flight_id):
    db.flights.delete_one({'_id': ObjectId(flight_id)})
    return redirect('flights_report')

# Update Booking Details
def update_booking(request, booking_id):
    if request.method == 'POST':
        flight = request.POST['flight']
        passenger_name = request.POST['passenger_name']
        db.bookings.update_one(
            {'_id': ObjectId(booking_id)}, 
            {"$set": {"flight": flight, "passenger_name": passenger_name}}
        )
        return redirect('admin_dashboard')

    booking = db.bookings.find_one({'_id': ObjectId(booking_id)})
    return render(request, 'update_booking.html', {'booking': booking})

# Remove Booking
def remove_booking(request, booking_id):
    db.bookings.delete_one({'_id': ObjectId(booking_id)})
    return redirect('admin_dashboard')

import csv

from django.http import HttpResponse

def download_flight_report(request):
    # Query all flights from MongoDB
    flights = db.flights.find()

    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="flight_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Flight Number', 'Departure City', 'Arrival City', 'Departure Time', 'Arrival Time', 'Price', 'Total Seats'])  # Header row

    for flight in flights:
        writer.writerow([flight.get('flight_number'), flight.get('departure_city'), flight.get('arrival_city'),
                         flight.get('departure_time'), flight.get('arrival_time'), flight.get('price'), flight.get('total_seats')])  # Data rows

    return response


from django.shortcuts import render

def streamlit_app(request):
    return render(request, 'streamlit_app.html')
