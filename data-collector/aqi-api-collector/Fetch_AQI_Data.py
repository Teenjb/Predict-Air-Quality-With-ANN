import requests
import time
import csv
from datetime import datetime

# API endpoint and token
api_url = "https://api.waqi.info/feed/geo:-6.26;106.88/?token=8148e322b23d220c53b71aa12885a647d490283e"

# Output CSV file
csv_file = 'air_quality_data.csv'

# Function to fetch data from API
def fetch_data():
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'ok':
            return data['data']
        else:
            print("Error in response data:", data)
            return None
    else:
        print("Failed to fetch data:", response.status_code)
        return None

# Function to extract required data fields
def extract_data(data):
    api_time = data['time']['iso']
    aqi = data['aqi']
    pm10 = data['iaqi'].get('pm10', {}).get('v', None)
    now_time = datetime.now().isoformat()
    return [now_time, api_time, aqi, pm10]

# Function to write data to CSV file
def write_to_csv(data):
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Initialize CSV file with headers
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Now Timestamp', 'API Timestamp', 'AQI', 'PM10'])

# Main loop to fetch and save data every minute
try:
    while True:
        data = fetch_data()
        if data:
            extracted_data = extract_data(data)
            write_to_csv(extracted_data)
            print(f"Data saved: {extracted_data}")
        time.sleep(60)  # Wait for 1 minute
except KeyboardInterrupt:
    print("Script terminated by user.")
