import json
def append_to_json_file(file_path, new_item):
    # Read the existing data from the JSON file
    try:
        with open(file_path, 'r') as file:
            data_json = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        data_json = []

    # Append the new item
    data_json.append(new_item)

    # Write the updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(data_json, file, indent=4)