import json

input_file_path = "./mock/aircrafts.json"
with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as json_file:
    original_data = json.load(json_file)

transformed_data = []
id_counter = 1
for i in range(300):
    number = 100 + i + 1
    code = f"VN-{number}"
    transformed_item = {
        "model": "aviation.aircraft",
        "pk": id_counter,
        "fields": {
            "model": original_data[i % len(original_data)]["model"],
            "capacity": original_data[i % len(original_data)]["capacity"],
            "code": code,
        },
    }
    transformed_data.append(transformed_item)
    id_counter += 1

output_file_path = "./aviation/fixtures/0001_Aircraft.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
