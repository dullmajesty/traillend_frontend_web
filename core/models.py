from django.db import models
from django.contrib.auth.models import User
import uuid


class Item(models.Model):
    CATEGORY_CHOICES = [
        ('Seating', 'Seating'),
        ('Tables', 'Tables'),
        ('Tent', 'Tent'),
        ('Venues', 'Venues'),
        ('Sport Equipment', 'Sport Equipment'),
        ('Cooling Ventilation', 'Cooling Ventilation'),
        ('Water Supply', 'Water Supply'),
        ('Electrical Accessories', 'Electrical Accessories'),
        ('Audio-Visual Equipment', 'Audio-Visual Equipment'),
        ('Transportation', 'Transportation'),
    ]

    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    def __str__(self):
        return self.name
    

class Item(models.Model):
    name = models.CharField(max_length=255)
    qty = models.IntegerField(default=0)  # or quantity? check this
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    
class Reservation(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    blocked = models.BooleanField(default=False)

    def __str__(self):
        status = "Blocked" if self.blocked else "Available"
        return f"{self.item.name} - {self.date} ({status})"


