import json

# file JSON airport
input_file_path = "./mock/airports.json"

# data từ file JSON airport
with open(input_file_path, "r", encoding="utf-8", errors="ignore") as json_file:
    original_data = json.load(json_file)

# Khởi tạo biến đếm ID
i = 0

# Khởi tạo danh sách chứa dữ liệu đã được chuyển đổi
transformed_data = []

# Duyệt qua mỗi item trong dữ liệu gốc và chuyển đổi thành định dạng mới
for item in original_data:
    i += 1

    # Tạo data từ dữ liệu ban đầu
    transformed_item = {
        "model": "aviation.airport",
        "pk": i,
        "fields": {
            "code": item["code"],
            "name": item["name"],
            "city": item["city"],
            "latitude": item["latitude"],
            "longitude": item["longitude"],
        },
    }

    # Thêm vào danh sách
    transformed_data.append(transformed_item)

output_file_path = "./aviation/fixtures/0002_Airport.json"

# Ghi dữ liệu đã chuyển đổi vào file JSON đầu ra
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(transformed_data, json_file, indent=2, ensure_ascii=False)

print(f"Transformed data saved to {output_file_path}")
