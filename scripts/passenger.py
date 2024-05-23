import json
import random
from faker import Faker
from vn_fullname_generator import generator
from dotenv import load_dotenv

load_dotenv()

# Dùng thư viện vn_fullname_generator để tạo tên người dùng
# Dùng Faker để tạo dữ liệu giả cho tên, email, và số điện thoại
fake = Faker("vi_VN")


transformed_data = []

# tạo dữ liệu cho 2000 hành khách
for i in range(2000):
    name = generator.generate(i % 2)  # Tạo tên dựa trên giới tính
    email = fake.email()
    phone = "+84" + str(fake.random_number(digits=9))
    citizen_identify_id = fake.random_number(digits=15)

    # Tạo ngày sinh
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=100)

    # Tạo giới tính (M, F, hoặc O)
    sex_choices = ["M", "F", "O"]
    weights = [0.48, 0.48, 0.02]  # gán xác suất cho giới tính
    sex = random.choices(sex_choices, weights=weights)[0]

    relation_id = None

    # Tạo ID liên quan với xác suất mặc định là 0.8
    if i > 0:
        probability_of_null = 0.8
        random_number = random.random()
        if random_number < probability_of_null:
            relation_id = None
        else:
            relation_id = fake.random_int(min=1, max=i)

    # Tạo một dict cho mỗi hành khách
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

    # thêm vào danh sách
    transformed_data.append(transformed_item)

# Ghi dữ liệu biến đổi vào một tệp JSON
output_file_path = "./aviation/fixtures/0003_Passenger.json"
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(transformed_data, json_file, indent=2, ensure_ascii=False)

print(f"Transformed data saved to {output_file_path}")
