import json
from urllib.parse import parse_qs, urlparse
import requests
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time


load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_CLIENT = os.getenv('SECRET_CLIENT')
MAIL = os.getenv('STRAVA_MAIL')
PASSWORD = os.getenv('STRAVA_PASSWORD')

auth_url = f"https://www.strava.com/oauth/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri=http://localhost/exchange_token&response_type=code&scope=activity:read"

chrome_driver_path = "/usr/lib/chromium-browser/chromedriver"

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
# chrome_options.add_argument("--disable-gpu")  # Disable GPU usage
# chrome_options.add_argument("--no-sandbox")  # Sandbox issues
# chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

# Initialize the ChromeDriver with options
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

def get_access_token(code):
    """
    Performs a GET request to get the access token .
    :param secret_client: API secret client
    :param code: API code
    :return: Response Access token
    """
    url = "https://www.strava.com/oauth/token"

    payload = json.dumps({
    "client_id": CLIENT_ID,
    "client_secret": SECRET_CLIENT,
    "code": code,
    "grant_type": "authorization_code"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()['access_token']

def get_code():
    try:
        driver.get(auth_url)
        time.sleep(2)

        print("Inserting email")
        # for _ in range(5):
        #     try:
        #         login_button = driver.find_element(By.ID, "mobile-login-button")
        #     except:
        #         break
        #     email_input = driver.find_element(By.ID, "mobile-email")
        #     email_input.send_keys(MAIL) 
            
        #     print("waiting to access email, 5 seconds left")
        #     time.sleep(5)
        #     email_input.send_keys(Keys.ENTER)
        #     time.sleep(2)

        # print("Mail step passed successfully")
        # print("Inserting password")
        # for _ in range(3):
        #     try:
        #         password_input = driver.find_element(By.NAME, "password")
        #     except:
        #         break
        #     password_input.send_keys(PASSWORD)
        #     password_input.send_keys(Keys.ENTER)
        #     time.sleep(3)

        print("Logged in")
        try:
            authorize_button = driver.find_element(By.ID, "authorize")
            authorize_button.click()
            time.sleep(3)
        except:
            print("No authorization button found; already authorized.")
        print("Authorization granted, processing code")

        current_url = driver.current_url
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)

        code = query_params.get("code", [None])[0]

        return code
     
    finally:
        driver.quit()