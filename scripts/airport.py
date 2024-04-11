import json

input_file_path = "./mock/airports.json"
with open(input_file_path, "r") as json_file:
    original_data = json.load(json_file)

i = 0
transformed_data = []
for item in original_data:
    i += 1
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
    transformed_data.append(transformed_item)

output_file_path = "./aviation/fixtures/0002_Airport.json"
with open(output_file_path, "w", encoding="utf-8") as json_file:
    json.dump(transformed_data, json_file, indent=2, ensure_ascii=False)

print(f"Transformed data saved to {output_file_path}")
