import json
import aiofiles
import asyncio

file_lock = asyncio.Lock()

async def append_to_json_file( new_item):
    file_path="data.json"
    async with file_lock:
        try:
            # Read the existing data from the JSON file
            async with aiofiles.open(file_path, 'r') as file:
                try:
                    data_json = json.loads(await file.read())
                except:
                    data_json = []
        except FileNotFoundError:
            print(f"Error: {file_path} file not found")
            data_json = []
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from {file_path}: {e}")
            data_json = []
        except Exception as e:
            print(f"Error: An unexpected error occurred while reading {file_path}: {e}")
            data_json = []

        # Append the new item
        data_json.append(new_item)

        # Write the updated data back to the JSON file
        try:
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(json.dumps(data_json, indent=4))
        except Exception as e:
            print(f"Error: An unexpected error occurred while writing to {file_path}: {e}")

async def append_to_json_file_error( new_item):
    file_path="data_with_error.json"
    async with file_lock:
        try:
            # Read the existing data from the JSON file
            async with aiofiles.open(file_path, 'r') as file:
                try:
                    data_json = json.loads(await file.read())
                except:
                    data_json = {}
        except FileNotFoundError:
            print(f"Error: {file_path} file not found")
            data_json = {}
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from {file_path}: {e}")
            data_json = {}
        except Exception as e:
            print(f"Error: An unexpected error occurred while reading {file_path}: {e}")
            data_json = {}

        # Append the new item
        data_json.update(new_item)

        # Write the updated data back to the JSON file
        try:
            async with aiofiles.open(file_path, 'w') as file:
                await file.write(json.dumps(data_json, indent=4))
        except Exception as e:
            print(f"Error: An unexpected error occurred while writing to {file_path}: {e}")



# import asyncio
# import motor.motor_asyncio

# import urllib.parse

# from pymongo import MongoClient
# from pymongo.server_api import ServerApi

# # MongoDB connection URI and database/collection names
# uri = "your_mongodb_atlas_uri"

# # Your raw username and password
# raw_username = "darshakmainz"
# raw_password = "Darshak1310@"

# # URL-encode the username and password
# encoded_username = urllib.parse.quote_plus(raw_username)
# encoded_password = urllib.parse.quote_plus(raw_password)

# # Construct the MongoDB URI
# uri = f"mongodb+srv://{encoded_username}:{encoded_password}@manga.tu41ccq.mongodb.net/?retryWrites=true&w=majority"

# database_name = "manga"
# collection_name = "all_manga"
# error_collection_name = "error_manga"

# # Create an instance of the MongoDB client
# client = motor.motor_asyncio.AsyncIOMotorClient(uri)
# db = client[database_name]
# collection = db[collection_name]
# error_collection = db[error_collection_name]

# async def append_to_mongodb(new_item):
#     try:
#         # Insert the new item into the collection
#         await collection.insert_one(new_item)
#     except Exception as e:
#         print(f"Error: An unexpected error occurred while inserting into MongoDB: {e}")

# async def append_to_mongodb_error(new_item):
#     try:
#         # Insert the new item into the error collection
#         await error_collection.insert_one(new_item)
#     except Exception as e:
#         print(f"Error: An unexpected error occurred while inserting into MongoDB: {e}")

