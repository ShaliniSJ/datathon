# Initialize the OpenCage geocoder with your API key
#api_key = '53184f9bf0e04720afd86b13e7752aa9'
import json
from geopy.geocoders import Nominatim
from time import sleep

# Initialize Nominatim API
geolocator = Nominatim(user_agent="myGeocoder")

# Define a function to geocode a query
def geocode_query(location_query):
    try:
        location = geolocator.geocode(location_query)
        return (location.latitude, location.longitude) if location else (None, None)
    except Exception as e:
        print(f"Error geocoding {location_query}: {e}")
        return None, None

# Load your place names (assuming you have a list of locations)
with open('C:\\Users\\Legion\\Desktop\\KSP DATATHON\\datathon\\functional_components\\images\\places_for_geocoding.txt', 'r') as file:
    place_names = file.read().splitlines()

geocoded_data = []
for place in place_names:
    lat, lon = geocode_query(place)
    if lat and lon:
        geocoded_data.append({'place': place, 'latitude': lat, 'longitude': lon})
    sleep(1)  # Respect the usage policy (1 request per second)

# Save the geocoded data to a JSON file
with open('geocoded_data.json', 'w') as file:
    json.dump(geocoded_data, file, indent=4)

print("Geocoding complete. Data saved to 'geocoded_data.json'.")
