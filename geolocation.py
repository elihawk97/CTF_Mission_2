import numpy as np
from geopy.geocoders import Nominatim

# Initialize Nominatim client
geolocator = Nominatim(user_agent="geoapiExercises")

# Example MAC addresses and corresponding latitudes
mac_addresses = [
    '00:1A:2B:3C:4D:5E',
    '01:1B:2C:3D:4E:5F',
    '02:2C:3D:4E:5F:6A'
]
latitudes = [21.028733554378693, 21.028733554378693, 21.028733554378693]  # Example latitudes

# Convert MAC addresses to longitudes
def mac_to_longitude(mac):
    try:
        parts = mac.split(':')
        last_byte = int(parts[-1], 16)
        return (last_byte - 128) * 0.1
    except ValueError as e:
        print(f"Error converting MAC address {mac}: {e}")
        return None

longitudes = [mac_to_longitude(mac) for mac in mac_addresses if mac_to_longitude(mac) is not None]
longitudes = [105.83028129882555, 105.83028129882555, 105.83028129882555]
if len(longitudes) == 0:
    raise ValueError("No valid longitudes found. Please check the MAC addresses.")

# Triangulate the point of interest
def triangulate(latitudes, longitudes):
    lat = np.mean(latitudes)
    lon = np.mean(longitudes)
    return lat, lon

lat_point_of_interest, lon_point_of_interest = triangulate(latitudes, longitudes)

# Adjust the coordinates if needed
def adjust_coordinates(lat, lon, lat_shift, lon_shift):
    return lat + lat_shift, lon + lon_shift

# Example shifts
lat_shift = 0.01
lon_shift = 0.01

adjusted_lat, adjusted_lon = adjust_coordinates(lat_point_of_interest, lon_point_of_interest, lat_shift, lon_shift)

# Find the location name using Nominatim
def find_location_name(lat, lon):
    location = geolocator.reverse((33.71259837310654, 73.03283493301709), language='en')
    return location.address if location else "Unknown location"

location_name = find_location_name(adjusted_lat, adjusted_lon)

print(f"Point of Interest Coordinates: Latitude: {lat_point_of_interest}, Longitude: {lon_point_of_interest}")
print(f"Adjusted Coordinates: Latitude: {adjusted_lat}, Longitude: {adjusted_lon}")
print(f"Location Name: {location_name}")
