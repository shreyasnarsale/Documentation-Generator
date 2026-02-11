from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.flight_number} from {self.origin} to {self.destination}"