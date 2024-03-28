import json
from faker import Faker
from vn_fullname_generator import generator
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker('vi_VN')
num_records = int(os.getenv('NUM_PASSENGERS'))
transformed_data = []

for i in range(num_records):
    name = generator.generate(i%2)
    email = fake.email()
    phone = "+84" + str(fake.random_number(digits=9))
    citizen_identify_id = fake.random_number(digits=15)
    passport_id = fake.random_number(digits=15)
    relation_id = None
    if i > 0:
        relation_id = fake.random_int(min=1, max=i)
    transformed_item = {
        "model": "aviation.passenger",
        "pk": i + 1,
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

output_file_path = "./aviation/fixtures/0002_Passenger.json"
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(transformed_data, json_file, indent=2, ensure_ascii=False)

print(f"Transformed data saved to {output_file_path}")
