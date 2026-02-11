import os
import streamlit as st
from langchain_community.llms import Ollama
from pymongo import MongoClient
from dotenv import load_dotenv
import plotly.express as px
from collections import Counter

# Load environment variables
load_dotenv()

# MongoDB Setup
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['airline_reservation_system']

# Collections
users_collection = db["users"]
flights_collection = db["flights"]
bookings_collection = db["bookings"]
payments_collection = db["payments"]

# Streamlit Layout
st.title("Airline Reservation DataBot")
st.sidebar.header("Navigation")
page = st.sidebar.selectbox("Choose a section", [
    "Booking Analytics",
    "Payment Analytics",
    "User Insights",
    "Demographic Insights",
    "Ask a Question"
])

# Function to load data
def load_bookings_data():
    return list(bookings_collection.find())

def load_payments_data():
    return list(payments_collection.find())

def load_flights_data():
    return list(flights_collection.find())

def load_users_data():
    return list(users_collection.find())

# Booking Analytics Page
if page == "Booking Analytics":
    st.header("Booking Analytics")
    
    bookings = load_bookings_data()
    if bookings:
        # Booking Count by Date
        booking_dates = [booking['bookingDate'].date() for booking in bookings]
        counts_by_date = Counter(booking_dates)
        
        # Create DataFrame for plotting
        df_bookings = {"Date": list(counts_by_date.keys()), "Bookings": list(counts_by_date.values())}
        fig_bookings = px.line(df_bookings, x="Date", y="Bookings", title="Daily Bookings")
        st.plotly_chart(fig_bookings)

        # Most Frequently Booked Routes
        route_counts = Counter()
        for booking in bookings:
            flight_id = booking['flight_id']
            flight = flights_collection.find_one({"_id": flight_id})
            if flight:
                route = f"{flight['departure_city']} to {flight['arrival_city']}"
                route_counts[route] += 1
        
        top_routes = route_counts.most_common(5)
        st.subheader("Top 5 Most Frequently Booked Routes")
        st.table(top_routes)

    else:
        st.write("No booking data available.")

# Payment Analytics Page
if page == "Payment Analytics":
    st.header("Payment Analytics")
    
    payments = load_payments_data()
    if payments:
        payment_status_counts = Counter(payment['payment_status'] for payment in payments)

        # Create DataFrame for plotting
        df_payments = {"Status": list(payment_status_counts.keys()), "Count": list(payment_status_counts.values())}
        fig_payments = px.bar(df_payments, x="Status", y="Count", title="Payment Status Counts")
        st.plotly_chart(fig_payments)
    else:
        st.write("No payment data available.")

# User Insights Page
if page == "User Insights":
    st.header("User Insights")
    
    users = load_users_data()
    if users:
        user_counts = Counter(user['role'] for user in users)
        st.subheader("User Role Counts")
        st.write(user_counts)
    else:
        st.write("No user data available.")

# Demographic Insights Page
if page == "Demographic Insights":
    st.header("Demographic Insights")
    
    bookings = load_bookings_data()
    if bookings:
        age_counts = Counter()
        gender_counts = Counter()
        
        for booking in bookings:
            for passenger in booking.get('passenger_details', []):
                age_counts[passenger['age']] += 1
                gender_counts[passenger['gender']] += 1
        
        # Age Distribution
        df_age = {"Age": list(age_counts.keys()), "Count": list(age_counts.values())}
        fig_age = px.bar(df_age, x="Age", y="Count", title="Passenger Age Distribution")
        st.plotly_chart(fig_age)

        # Gender Distribution
        df_gender = {"Gender": list(gender_counts.keys()), "Count": list(gender_counts.values())}
        fig_gender = px.pie(df_gender, names="Gender", values="Count", title="Passenger Gender Distribution")
        st.plotly_chart(fig_gender)
    else:
        st.write("No booking data available.")

# Ask a Question Page
if page == "Ask a Question":
    st.header("Ask about Airline Reservations")
    
    user_query = st.text_input("Enter your question:")
    if user_query:
        try:
            # Use Ollama for LLM query (make sure this is correctly set up)
            prompt = f"Please provide details about: {user_query}"
            response = Ollama(model='tinyllama', prompt=prompt)
            st.write(response)
        except Exception as e:
            st.write(f"Error querying the model: {str(e)}")
