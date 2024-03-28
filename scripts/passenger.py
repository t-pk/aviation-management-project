import json
from faker import Faker
from vn_fullname_generator import generator

fake = Faker('vi_VN')
import random

def generate_vietnam_phone_number():
    """
    Generate a random phone number in the format used in Vietnam.
    """
    # Select a random format
    formats = [
        "03xxxxxxxx",  # Mobile numbers starting with 03
        "07xxxxxxxx",  # Mobile numbers starting with 07
        "08xxxxxxxx",  # Mobile numbers starting with 08
        "09xxxxxxxx",  # Mobile numbers starting with 09
        "02xxxxxxxx",  # Landline numbers starting with 02
    ]
    
    # Randomly select a format
    phone_format = random.choice(formats)
    
    # Generate a phone number based on the selected format
    phone_number = ''.join(random.choices('0123456789', k=len(phone_format)))
    
    # Insert dashes if the format requires them
    if '.' in phone_format:
        phone_number = ''.join(
            char if char != 'x' else random.choice('0123456789')
            for char in phone_format
        )
    
    return phone_number

num_records = 1000  # Change this to the desired number of records

transformed_data = []

for i in range(num_records):
    # Generate fake data
    name = generator.generate(i%2)
    email = fake.email()
    phone = "+84" + generate_vietnam_phone_number()
    citizen_identify_id = fake.random_number(digits=15)
    passport_id = fake.random_number(digits=15)

    # For relation field, we'll randomly set it to another passenger's ID
    relation_id = None
    if i > 0:
        # Randomly select another passenger's ID as relation
        relation_id = fake.random_int(min=1, max=i)

    # Create a transformed item
    transformed_item = {
        "model": "aviation.passenger",
        "pk": i + 1,  # Assuming IDs start from 1
        "fields": {
            "name": name,
            "email": email,
            "phone": phone,
            "citizen_identify_id": citizen_identify_id,
            "passport_id": passport_id,
            "relation": relation_id,
        }
    }

    transformed_data.append(transformed_item)

# Save transformed data to a JSON file
output_file_path = "./aviation/fixtures/0002_Passenger.json"
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(transformed_data, json_file, indent=2, ensure_ascii=False)

print(f"Transformed data saved to {output_file_path}")
