from datetime import datetime
import time
from constants import important_data


def get_unix_timestamp(date_string, date_format="%Y-%m-%d"):
    """
    Converts a date string to a UNIX timestamp.
    :param date_string: Date in string format (e.g., '2025-01-17')
    :param date_format: Format of the input date string (default: '%Y-%m-%d')
    :return: UNIX timestamp as an integer
    """
    try:
        dt = datetime.strptime(date_string, date_format)
        return int(time.mktime(dt.timetuple()))
    except ValueError as e:
        print(f"Error: {e}")
        return None
    

# Conversion functions for different metrics
def convert_speed(speed_in_mps):
    """Convert speed from meters per second to kilometers per hour."""
    return speed_in_mps * 3.6

def convert_distance(distance_in_m):
    """Convert distance from meters to kilometers."""
    return distance_in_m / 1000

def convert_time(time_in_seconds):
    """Convert time from seconds to minutes."""
    return time_in_seconds / 60



# Conversion dictionary where keys are metric names and values are the conversion functions
conversion_dict = {
    "average_speed": convert_speed,
    "distance": convert_distance,
    "moving_time": convert_time,
    "elapsed_time":convert_time
}

def parse_data(data):
    for train in data:
        keys_to_keep = {key: train[key] for key in important_data if key in train}
        train.clear()  # Clear the dictionary
        train.update(keys_to_keep) 
    return data

# Function to convert all metrics in a dictionary
def convert_metrics(d, conversion_dict):
    """Convert the metrics in the given dictionary based on the conversion dictionary."""
    for key, value in d.items():
        if key in conversion_dict:
            # Apply the corresponding conversion function for specific metrics
            d[key] = conversion_dict[key](value)
    return d