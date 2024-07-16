import json

def append_to_json_file(file_path, new_item):
    try:
        # Read the existing data from the JSON file
        with open(file_path, 'r') as file:
            data_json = json.load(file)
    except FileNotFoundError:
        print(f"Error: {file_path} file not found")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from {file_path}: {e}")
        return
    except Exception as e:
        print(f"Error: An unexpected error occurred while reading {file_path}: {e}")
        return

    # Append the new item
    data_json.append(new_item)

    # Write the updated data back to the JSON file
    try:
        with open(file_path, 'w') as file:
            json.dump(data_json, file, indent=4)
    except Exception as e:
        print(f"Error: An unexpected error occurred while writing to {file_path}: {e}")

# Example usage
new_data = {"key": "value"}
append_to_json_file("data.json", new_data)
