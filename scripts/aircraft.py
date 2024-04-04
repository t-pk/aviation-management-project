import json

input_file_path = "./mock/aircrafts.json"
with open(input_file_path, "r") as json_file:
    original_data = json.load(json_file)

transformed_data = []
for item in original_data:
    transformed_item = {
        "model": "aviation.aircraft",
        "pk": item["id"],
        "fields": {
            "model": item["model"],
            "capacity": item["capacity"],
            "code": item["code"],
        },
    }
    transformed_data.append(transformed_item)

output_file_path = "./aviation/fixtures/0001_Aircraft.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
