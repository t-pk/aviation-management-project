import json

# file JSON aircraft
input_file_path = "./mock/aircrafts.json"

# data từ file JSON aircraft
with open(input_file_path, "r", encoding="utf-8", errors="ignore") as json_file:
    original_data = json.load(json_file)

# Khởi tạo danh sách
transformed_data = []
id_counter = 1

# Tạo ra 300 máy bay
for i in range(300):
    number = 100 + i + 1
    code = f"VN-{number}"

    # Tạo data từ dữ liệu ban đầu
    transformed_item = {
        "model": "aviation.aircraft",
        "pk": id_counter,
        "fields": {
            "model": original_data[i % len(original_data)]["model"],
            "capacity": original_data[i % len(original_data)]["capacity"],
            "code": code,
        },
    }

    # Thêm vào danh sách
    transformed_data.append(transformed_item)
    id_counter += 1

output_file_path = "./aviation/fixtures/0001_Aircraft.json"

# Ghi dữ liệu đã chuyển đổi vào file JSON đầu ra
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
