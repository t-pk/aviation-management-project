import json

# Read original data from JSON file
input_file_path = "./mock/passengers.json"
with open(input_file_path, "r") as json_file:
    original_data = json.load(json_file)

# Transform data into desired format
transformed_data = []
for item in original_data:
    transformed_item = {
        "model": "aviation.passenger",
        "pk": item["id"],
        "fields": {
            "name": item["name"], 
            "email":  item["email"],
            "phone":  item["phone"],
        }
    }
    transformed_data.append(transformed_item)

# Save transformed data to a JSON file
output_file_path = "./aviation/fixtures/0002_Passenger.json"
with open(output_file_path, "w") as json_file:
    json.dump(transformed_data, json_file, indent=2)

print(f"Transformed data saved to {output_file_path}")
