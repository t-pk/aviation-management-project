import json
import random
from faker import Faker
from vn_fullname_generator import generator

fake = Faker("vi_VN")
transformed_data = []

for i in range(4000):
    name = generator.generate(i % 2)
    email = fake.email()
    phone = "+84" + str(fake.random_number(digits=9))
    citizen_identify_id = fake.random_number(digits=15)
    relation_id = None

    # Generate date_of_birth
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=100)
    # Generate sex
    sex_choices = ["M", "F", "O"]
    weights = [0.48, 0.48, 0.02]  # 48% chance for "M" and "F", 2% chance for "O"
    sex = random.choices(sex_choices, weights=weights)[0]

    if i > 0:
        probability_of_null = 0.8  # Example: 80% probability of null
        random_number = random.random()
        if random_number < probability_of_null:
            relation_id = None
        else:
            relation_id = fake.random_int(min=1, max=i)

    transformed_item = {
        "model": "aviation.passenger",
        "pk": i + 1,
        "fields": {
            "name": name,
            "email": email,
            "phone": phone,
            "citizen_identify_id": citizen_identify_id,
            "relation": relation_id,
            "date_of_birth": str(date_of_birth),
            "sex": sex,
        },
    }

    transformed_data.append(transformed_item)

output_file_path = "./aviation/fixtures/0003_Passenger.json"
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(transformed_data, json_file, indent=2, ensure_ascii=False)

print(f"Transformed data saved to {output_file_path}")
