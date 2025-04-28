import requests
import json
from pprint import pprint
from access_token import get_access_token, get_code
from utils import get_unix_timestamp, conversion_dict, parse_data, convert_metrics
from dotenv import load_dotenv
import os


load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def fetch_data(access_token, unix_timestamp):
    """
    Performs a GET request to fetch data based on the access token and UNIX timestamp.
    :param access_token: API access token
    :param unix_timestamp: Start date in UNIX timestamp format
    :return: Response JSON or error message
    """
    # Define the endpoint (replace with the actual endpoint URL)
    endpoint = "https://www.strava.com/api/v3/athlete/activities"

    # Set up the request headers and parameters
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "after": unix_timestamp,  # Fetch data after this timestamp
        "per_page": 50,  # Number of activities per page (adjust as needed)
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def main():
    # FIRST GO TO THE LINK BELLOW AND GET YOUR CODE
    # https://www.strava.com/oauth/authorize?client_id=YOR_CLIENT_ID&response_type=code&redirect_uri=http://localhost/exchange_token&response_type=code&scope=activity:read
    code = get_code()
    access_token = get_access_token(code)
    date_string = input("Enter the date (YYYY-MM-DD): ").strip()

    # access_token = get_access_token()
    # Convert date to UNIX timestamp
    unix_timestamp = get_unix_timestamp(date_string)
    if unix_timestamp is None:
        print("Invalid date. Exiting...")
        return

    # Fetch data
    print(
        f"Fetching data for activities after {date_string} (UNIX: {unix_timestamp})..."
    )
    data = fetch_data(access_token, unix_timestamp)

    # Display the result
    if data:
        print("Data fetched successfully:")
        data = parse_data(data)
        for metrics in data:
            convert_metrics(metrics, conversion_dict)
        for train in data:
            pprint(train)
    else:
        print("Failed to fetch data.")


if __name__ == "__main__":
    main()
