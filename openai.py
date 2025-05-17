import csv
import random
from faker import Faker

# Initialize Faker for generating realistic names and locations
fake = Faker()

# List of blue collar job positions
blue_collar_jobs = [
    "Construction Worker",
    "Electrician",
    "Plumber",
    "Carpenter",
    "Welder",
    "Auto Mechanic",
    "HVAC Technician",
    "Machine Operator",
    "Truck Driver",
    "Warehouse Worker",
    "Maintenance Technician",
    "Factory Worker",
    "Painter",
    "Landscaper",
    "Equipment Operator"
]

# Generate 100 fake candidates
candidates = []
for _ in range(100):
    candidate = {
        'firstname': fake.first_name(),
        'lastname': fake.last_name(),
        'job_position': random.choice(blue_collar_jobs),
        'location': fake.city() + ", " + fake.state_abbr()
    }
    candidates.append(candidate)

# Write to CSV file
csv_filename = 'blue_collar_candidates.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    fieldnames = ['firstname', 'lastname', 'job_position', 'location']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for candidate in candidates:
        writer.writerow(candidate)

print(f"Generated {len(candidates)} candidates and saved to {csv_filename}")
