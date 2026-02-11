# from django.shortcuts import render

# Create your views here.


# Create your views here.

# payment/views.py
import razorpay
# from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=('rzp_test_zxL57CWrx3zkB0', 'YXhsMCw5sDCeHeMAk9mIc0t0'))



# Use the connection string from MongoDB Atlas
client = MongoClient('mongodb+srv://youtubepy:youtubepy@cluster0.hlekbr4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# Choose the database to use
db = client['airline_reservation_system']

# try:
#     db.command('ping')
#     print("Connected to MongoDB")
# except Exception as e:
#     print(f"Error connecting to MongoDB : {e}")

flights = db['flights']
users = db['users']
bookings = db['bookings']
payment_collection = db['payments']
special_services = db['special_services']

from django.core.mail import send_mail
from django.conf import settings

def send_booking_confirmation_email(user_email, booking_id):
    subject = 'Booking Confirmation'
    message = f'Your booking was successful! Your Booking ID is {booking_id}. Thank you for choosing Air India!'
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twilio Setup
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

def send_booking_confirmation_sms(phone_number, booking_id):
    # Create a Twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Create the message
    message = client.messages.create(
        body=f'Your booking was successful! Your Booking ID is {booking_id}.Thank you for choosing Air India!',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    return message.sid


def payment_page(request, booking_id):

    b = db.bookings.find_one({"_id":ObjectId(booking_id)})
    f_id= b['flight_id']
    f = db.flights.find_one({"_id":ObjectId(f_id)})
    ss=b['special_services']
    # f = db.special_services.find_one({"_id":ObjectId(f_id)})

    # Define the order amount and currency
    amount = f['price']*100*b['num_passengers']# Amount in paise (INR 500)
    currency = 'INR'
    total_amount = int(amount/100)
    refund_fee = 0.2*total_amount

    # Create Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency, payment_capture='1'))

    # Send order details to the template
    context = {
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_key_id': 'rzp_test_zxL57CWrx3zkB0',
        'amount': amount,
        'total_amount': total_amount,
        'refund_fee': refund_fee,
        'booking_id':booking_id,
        'b':b,
        'f':f
    }

    return render(request, 'payment/payment_page.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        # Extract details from POST data
        razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        razorpay_signature = request.POST.get('razorpay_signature', '')
        booking_id = request.POST.get('booking_id', '')


        # Verify payment signature to ensure it's genuine
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            razorpay_client.utility.verify_payment_signature(params_dict)

            amount = int(request.POST.get('amount', ''))
            refund_fee = 0.2*amount

            payment_data = {'razorpay_payment_id':razorpay_payment_id, 'razorpay_order_id' :razorpay_order_id, 'amount': amount, 'refund_fee':refund_fee,'currency':request.POST.get('currency', 'INR'), 'booking_id':booking_id , 'payment_status':'Completed'}

            payment_collection.update_one({'booking_id':ObjectId(booking_id)},{'$set':payment_data}, upsert= True)
            bookings.update_one({'_id':ObjectId(booking_id)},{'$set':{'status':'Completed'}}, upsert= True)
            print(payment_data)
            # If payment is verified, display success message

            b = db.bookings.find_one({"_id":ObjectId(booking_id)})
            f_id= b['flight_id']
            f = db.flights.find_one({"_id":ObjectId(f_id)})
            passengers = b['passenger_details']
            num_passengers = b['num_passengers']
            passenger_names = {}
            for i in range(num_passengers):
                passenger_names[f"pass{i+1}"] = passengers[i]["name"]


            #email sending
            user_email = b['email']
            
            b_id = str(booking_id)            
            send_booking_confirmation_email(user_email, b_id)
            print('Email sent successfully')
            print(f'Booking ID: {b_id}, Email: {user_email}, , type of user_email: {type(user_email)}')

            # Assuming `b` contains user data and booking information
            # user_email = b['email']
          
            user_phone_number ="+91" + str(b['phone'])  # Ensure this is included in your user data
            # b_id = str(booking_id)
            
            sms_sid = send_booking_confirmation_sms(user_phone_number, b_id)
            print(f'SMS sent successfully, SID: {sms_sid}')
            print(f'Booking ID: {b_id}, Email: {user_email}, Phone: {user_phone_number}, Type of user_email: {type(user_email)}')


            return render(request, 'payment/success.html',{'b':b,'f':f, 'booking_id':booking_id,'amount':amount ,'refund_fee':refund_fee , 'passengers':passengers,'passenger_names':passenger_names})
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest("Payment verification failed")

    return HttpResponseBadRequest("Invalid request")
