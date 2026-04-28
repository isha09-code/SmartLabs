import os
import sys
import django
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab_booking.settings')
django.setup()

from booking.models import Equipment

# Define the new items
lab_data = [
    # PHYSICS
    {"name": "Digital Multimeter", "category": "physics", "quantity": 10},
    {"name": "Convex Lens (Set of 5)", "category": "physics", "quantity": 15},
    {"name": "Vernier Caliper", "category": "physics", "quantity": 12},
    {"name": "Ohm's Law Apparatus", "category": "physics", "quantity": 5},
    {"name": "Prism (Glass)", "category": "physics", "quantity": 20},
    
    # CHEMISTRY
    {"name": "Bunsen Burner", "category": "chemistry", "quantity": 8},
    {"name": "Titration Flask (250ml)", "category": "chemistry", "quantity": 25},
    {"name": "Digital Weighing Scale", "category": "chemistry", "quantity": 4},
    {"name": "Centrifuge Machine", "category": "chemistry", "quantity": 2},
    {"name": "PH Meter", "category": "chemistry", "quantity": 6},
    
    # BIOLOGY
    {"name": "Compound Microscope", "category": "biology", "quantity": 10},
    {"name": "Human Skeleton Model", "category": "biology", "quantity": 1},
    {"name": "Prepared Slides (Set)", "category": "biology", "quantity": 15},
    {"name": "Dissection Kit", "category": "biology", "quantity": 12},
    {"name": "Blood Pressure Monitor", "category": "biology", "quantity": 3},
    
    # COMPUTER
    {"name": "Arduino Uno Kit", "category": "computer", "quantity": 15},
    {"name": "Raspberry Pi 4", "category": "computer", "quantity": 8},
    {"name": "LAN Tester", "category": "computer", "quantity": 5},
    {"name": "External Hard Drive (1TB)", "category": "computer", "quantity": 10},
    {"name": "VR Headset", "category": "computer", "quantity": 2},
    
    # GEOGRAPHY
    {"name": "Digital Anemometer", "category": "geography", "quantity": 4},
    {"name": "Magnetic Compass", "category": "geography", "quantity": 20},
    {"name": "Barometer", "category": "geography", "quantity": 5},
    {"name": "Global Positioning System (GPS)", "category": "geography", "quantity": 3},
    {"name": "Topographic Maps Set", "category": "geography", "quantity": 10}
]

# Save to database
for item in lab_data:
    Equipment.objects.get_or_create(name=item['name'], category=item['category'], defaults={'quantity': item['quantity']})

print("Success! 25 Lab items added.")