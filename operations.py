import json
from datetime import datetime



# Function to load JSON data from a file
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Specify the path to your JSON file
json_file_path = 'data.json'

# Load the JSON data
data_list = load_json_data(json_file_path)

# Print the loaded data (for verification)
# print(json.dumps(data_list, indent=4))


# # Function to sort by latest (date)
def sort_by_latest(manga_list):
    return sorted(manga_list, key=lambda x: datetime.strptime(x['date'], '%m/%d/%Y'), reverse=True)

# Function to sort by rating
def sort_by_rating(manga_list):
    return sorted(manga_list, key=lambda x: float(x['rating']), reverse=True)

# Function to sort by trending (views in the last period)
# Assuming 'trending_views' field is added to each manga entry for this example
# def sort_by_trending(manga_list):
#     return sorted(manga_list, key=lambda x: x.get('trending_views', 0), reverse=True)

# Function to sort by most views
def sort_by_most_views(manga_list):
    return sorted(manga_list, key=lambda x: (x['Total views']), reverse=True)

# Example usage
sorted_by_latest = sort_by_latest(data_list)
sorted_by_rating = sort_by_rating(data_list)
# sorted_by_trending = sort_by_trending(data_list)
sorted_by_most_views = sort_by_most_views(data_list)

# Print sorted data (titles only for brevity)
print("Sorted by Latest:")
for manga in sorted_by_latest:
    print(manga['title'])

print("\nSorted by Rating:")
for manga in sorted_by_rating:
    print(manga['title'])

# print("\nSorted by Trending:")
# for manga in sorted_by_trending:
#     print(manga['title'])

print("\nSorted by Most Views:")
for manga in sorted_by_most_views:
    print(manga['title'])
