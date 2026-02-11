from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_number', 'airline', 'departure_city',
            'arrival_city', 'departure_time', 'arrival_time',
            'duration', 'price', 'total_seats'
        ]