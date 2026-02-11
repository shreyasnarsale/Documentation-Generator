from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, HttpResponse
from functools import wraps
from pymongo.errors import ConnectionError, ConfigurationError

import razorpay
from django.conf import settings

# from utils.mongo_connection import db


try:
    # Use the connection string from MongoDB Atlas
    client = MongoClient("mongodb+srv://youtubepy:youtubepy@cluster0.hlekbr4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    db = client['airline_reservation_system']
except (ConnectionError, ConfigurationError) as e:
    # Log the error and provide a response
    print("MongoDB Connection Error:", e)
    db = None  # Set db to None if there's a connection issue

# try:
#     db.command('ping')
#     print("Connected to MongoDB")
# except Exception as e:
#     print(f"Error connecting to MongoDB : {e}")

flights = db['flights']
users = db['users']
bookings = db['bookings']
payments = db['payments']
special_services = db['special_services']





# def adminpage(request):
#     # Since the login page verifies the user, we can assume the user is an admin if they are here

#     unique_departure_cities = flights.distinct('departure_city')
#     unique_arrival_cities = flights.distinct('arrival_city')

#     # Handle POST requests
#     if request.method == 'POST':
#         # Check for specific admin actions via hidden fields or form names
#         if 'add_flight' in request.POST:
#             return handle_add_flight(request)
#         elif 'generate_flight_report' in request.POST:
#             return generate_flight_report(request)
#         elif 'generate_employee_report' in request.POST:
#             return generate_employee_report(request)
#         elif 'search_flights' in request.POST:
#             return search_flights(request)

#     # Default context for displaying flight management options
#     items = list(flights.find())
#     for item in items:
#         item['id'] = str(item['_id'])

#     return render(request, 'admin_dashboard.html', {
#         'items': items,
#         'unique_departure_cities': unique_departure_cities,
#         'unique_arrival_cities': unique_arrival_cities,
#         'user_email': request.COOKIES.get('email'),  # Pass the email to the template if needed
#     })
    
#     # Redirect non-authenticated users to the home page (not needed as per your context)
#     return redirect('home')  # This line can be removed if all users here are authenticated


# def handle_add_flight(request):
#     """
#     Handle adding a new flight to the database.
#     """
#     departure_city = request.POST.get('departure_city')
#     arrival_city = request.POST.get('arrival_city')
#     flight_date = request.POST.get('flight_date')
#     price = request.POST.get('price')

#     # Ensure all required fields are present
#     if departure_city and arrival_city and flight_date and price:
#         new_flight = {
#             'departure_city': departure_city,
#             'arrival_city': arrival_city,
#             'flight_date': datetime.strptime(flight_date, "%Y-%m-%d"),
#             'price': float(price)
#         }
#         flights.insert_one(new_flight)
#         return redirect('adminpage')  # Redirect to the admin dashboard after adding a flight
#     else:
#         return render(request, 'add_flight.html', {'error': 'All fields are required!'})

# def add_page(request):
#     if request.method == 'POST':
#         # Handle form submission for adding a page here
#         pass  # Replace with your logic

#     return render(request, 'add_page.html')

# def generate_flight_report(request):
#     """
#     Generate a report of all flights in the system.
#     """
#     flight_data = list(flights.find())
#     for flight in flight_data:
#         flight['id'] = str(flight['_id'])

#     return render(request, 'flight_report.html', {'flights': flight_data})


# def generate_employee_report(request):
#     """
#     Generate a report of all employees.
#     """
#     employee_data = list(users.find({"role": "employee"}))
#     for emp in employee_data:
#         emp['id'] = str(emp['_id'])

#     return render(request, 'employee_report.html', {'employees': employee_data})


# def search_flights(request):
#     """
#     Search for flights based on departure and arrival cities.
#     """
#     departure_city = request.POST.get('departure_city')
#     arrival_city = request.POST.get('arrival_city')
#     items = list(flights.find({'departure_city': departure_city, 'arrival_city': arrival_city}))
#     for item in items:
#         item['id'] = str(item['_id'])

#     return render(request, 'results.html', {'items': items})

# def admin_dashboard(request):
#     # Logic to fetch any necessary data for the dashboard
#     return render(request, 'admin_dashboard.html') 


# def login_required(f):
#     @wraps(f)
#     def wrap(request, *args, **kwargs):
#         # Get user_id from the cookie
#         user_id = request.COOKIES.get('user_id')
        
#         if user_id:
#             # Check if the user exists in MongoDB
#             user = users.find_one({"_id": ObjectId(user_id)})
            
#             if user:
#                 # User is authenticated, proceed to the view
#                 request.user = user  # Optionally, pass the user object in the request
#                 return f(request, *args, **kwargs)
        
#         # If not authenticated, redirect to login
#         return HttpResponseRedirect('/login')
    
#     return wrap

# def manage_employees(request):
#     # Handle form submission for adding or updating employee records
#     if request.method == 'POST':
#         employee_name = request.POST.get('employee_name')
#         employee_email = request.POST.get('employee_email')
        
#         # Logic for adding or updating an employee record
#         # For example, you might create a new Employee object
#         if employee_name and employee_email:
#             # Employee.objects.create(name=employee_name, email=employee_email)  # Update this as needed

#             # Redirect to the same page to avoid re-submission
#             return redirect('manage_employees')

#     # Fetch existing employees to display them
#     # employees = Employee.objects.all()  # Replace with your logic to retrieve employees from the database

#     return render(request, 'manage_employees.html', {
#         # 'employees': employees,  # Pass the employees to the template
#     })


# from django.db import connection
# from django.http import HttpResponse

# from pymongo import MongoClient

# # Updated MongoDB URI
# # MONGO_URI = 'mongodb://youtubepy:youtubepy@localhost:27017/airline_database'  # Updated database name
# # client = MongoClient(MONGO_URI)

# # # Accessing the specific database and collection
# # db = client['airline_database']['flights']  # Only access the flights collection directly

# def add_flight(request):
#     message = ""
    
#     # Generate a random number as a placeholder functionality
#     random_number = random.randint(1, 100)
    
#     if request.method == "POST":
#         # Get form data (though it's not being used here)
#         flight_number = request.POST.get('flight_number')
#         departure_city = request.POST.get('departure_city')
#         arrival_city = request.POST.get('arrival_city')
#         departure_time = request.POST.get('departure_time')
#         arrival_time = request.POST.get('arrival_time')
#         price = request.POST.get('price')
#         total_seats = request.POST.get('total_seats')

#         # Instead of inserting into the database, just create a message with the random number
#         message = f"Random number generated: {random_number}. Flight details were received but not processed."

#     return render(request, 'add_flight.html', {'message': message})


# def success_page(request):
#     return render(request, 'success.html')


def home(request):

    user_id = request.COOKIES.get('user_id')
    
    if user_id:
        user = users.find_one({"_id": ObjectId(user_id)})
        if user:
            return render(request, 'home.html', {"user": user})

    items = list(flights.find())
    for item in items:
        item['id']=str(item['_id'])
    unique_departure_cities = flights.distinct('departure_city')
    unique_arrival_cities = flights.distinct('arrival_city')

    if request.method == 'POST':
        departure_city = request.POST.get('departure_city')
        arrival_city = request.POST.get('arrival_city')
        # flight = flights.find_one({'departure_city': departure_city})
        items = list(flights.find({'departure_city': departure_city, 'arrival_city': arrival_city}))
        
        print(f"\n\n ----- Checking Index ------\n\n { flights.find({'departure_city': departure_city, 'arrival_city': arrival_city}).explain() } \n\n")

        for item in items:
            item['id']=str(item['_id'])
        return render(request, 'results.html', {'items':items})
      
    
    return render(request, 'home.html', {'items': items , 'unique_departure_cities' : unique_departure_cities, 'unique_arrival_cities':unique_arrival_cities, 'user':None })
    


def results(request,items):
    flights = items
      # Fetch all flights from the collection
    return render(request, 'results.html', {'flights':flights})

def book(request, flight_id):
    # if not request.user.is_authenticated:
    #     return redirect('login')

    flight = db.flights.find_one({"_id": ObjectId(flight_id)})
    
    if request.method == "POST":
        # Get data from the form
        user_id = request.user.id
        extra_baggage = request.POST.get('extraBaggage')
        seat_number = request.POST.get('seatNumber')
          # Select multiple services
        
        booking_date = datetime.now()
        status = 'Pending'
        
        # Insert booking into MongoDB
        booking_id = db.bookings.insert_one({
            "user_id": user_id,
            "flight_id": flight_id,
            "extra_baggage": extra_baggage,
            "seat_number": seat_number,
            
            "bookingDate": booking_date,
            "status": status
        }).inserted_id
        
        # Redirect to payment or success page
        return redirect('passengers', booking_id=booking_id)

    return render(request, 'book.html', {"flight": flight})

def passengers(request, booking_id):
   
    # if not request.user.is_authenticated:
    #     return redirect('login')
    
    if request.method == "POST":
        num_passengers = int(request.POST.get('numPassengers'))
        
        # Collecting passenger details
        passengers = []
        for i in range(1, num_passengers + 1):
            name = request.POST.get(f'passenger{i}Name')
            age = request.POST.get(f'passenger{i}Age')
            gender = request.POST.get(f'passenger{i}Gender')
            
            if name and age and gender:
                passengers.append({
                    "name": name,
                    "age": int(age),
                    "gender": gender
                })
        
       
        special_services = request.POST.getlist('specialServices')  # Select multiple services
        # Collecting contact details
        # country =request.POST.get('country')
        contact_email = request.POST.get('email')
        contact_phone = request.POST.get('phone')
        
        # Save passengers and contact details to the booking
        db.bookings.update_one(
            {"_id": ObjectId(booking_id)},
            {
                "$set": {
                    "passenger_details": passengers,
                    "email": contact_email,
                    "phone": contact_phone,
                    # "country":country,
                    "special_services":special_services,
                    "num_passengers": num_passengers
                }
            }
        )
        
        # Redirect to payment page
        return redirect('payment_page', booking_id=booking_id)
    
    return render(request, 'passengers.html', {"booking_id": booking_id})



def success(request):
    pass

# client = MongoClient("mongodb://youtubepy:youtubepy@localhost:27017/")
# db = client['Airline_Database']['airline_reservation_system']['employees']

# def manage_employees(request):
#     # Fetch all employee data from the employees collection
#     employee_data = list(db.find())  # Convert cursor to list
#     return render(request, 'admin_panel.html', {'employees': employee_data})

# def add_employee(request):
#     if request.method == "POST":
#         name = request.POST['name']
#         email = request.POST['email']
#         position = request.POST['position']

#         # Insert employee into the database
#         db.insert_one({'name': name, 'email': email, 'position': position})
        
#         return redirect('manage_employees')  # Redirect to the manage employees page

# def delete_employee(request, employee_id):
#     if request.method == "POST":
#         # Delete the employee from the database
#         db.delete_one({'_id': employee_id})
#         return redirect('manage_employees')
    

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name') 
        password = request.POST.get('password')  # Hashing password
        
        # Check if user already exists
        if users.find_one({"email":email}):
            return render(request, 'register.html', {"error": "User already exists"})
        
        # Insert user into MongoDB
        users.insert_one({
            "name": name,
            "email": email,
            "password": password
        })
        return redirect('login')
    
    return render(request, 'register.html')



# def adminlogin(request):
#     error = None
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Debug logs
#         print(f"Email: {email}")
#         print(f"Password: {password}")

#         if not email.endswith('@airindia.org'):
#             error = "Email should end with @airindia.org"
#         elif password != '1212':
#             error = "Invalid Password"
#         else:
#             print("Login successful, redirecting to admin page.")
#             return redirect('adminpage')  # Ensure 'adminpage' is correctly defined

#     return render(request, 'adminlogin.html', {'error': error})



def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Fetch user from MongoDB
        user = users.find_one({"email": email})
        
        if user and (password == user['password']):
            
            # Return the user's MongoDB ID to be used as a token
            user_id = str(user['_id'])

                   
            return redirect('home')
        else:
            return render(request, 'login.html', {"error": "Invalid username or password"})
    
    return render(request, 'login.html')

def logout(request):
        
     return redirect('login')


def manage(request, booking_id):
    booking_id = None
    if request.method == 'POST':
        booking_id = request.POST.get('bookingReference')
        booking_data = db.bookings.find_one({"_id": ObjectId(booking_id)})
        
        return render(request, 'manage.html', {'booking_data': booking_data, 'booking_id': booking_id})
    
    return render(request, 'manage.html', {'booking_id': booking_id})



def experience(request):
    return render(request, 'Experience.html')       

def destination(request):
    return render(request, 'Destination.html')

def loyalty(request):
    return render(request, 'Loyality.html')  

def help(request):
    return render(request, 'Help.html') 

def spline(request):
    return render(request, 'spline.html')





