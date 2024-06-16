import csv
import os
from datetime import datetime, timedelta
from google.cloud import storage
from PIL import Image
import random
import matplotlib.pyplot as plt


def display_random_images(x, y):
    random_indices = random.sample(range(len(x)), 5)
    fig, axes = plt.subplots(1, 5, figsize=(20, 4))
    for i, index in enumerate(random_indices):
        axes[i].imshow(x[index])
        axes[i].axis('off')  # Hide the axis
        axes[i].set_title(f"PM10: {y[index]}")

    plt.show()

    # Get 5 unique random indices
    random_indices = random.sample(range(len(x)), 5)

    for index in random_indices:
        print(f"Entry {index + 1}:")
        print(f"x: {x[index]}")  # This will print the image object reference
        print(f"y: {y[index]}")  # This will print the PM100 value

# Function to download a file from Google Cloud Storage
def download_file_from_gcs(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client.from_service_account_json("ai-finpro-data-labeling-key.json")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} to {destination_file_name}.")

# Function to match images with the CSV data
def match_images_with_csv(csv_file_path, images_folder_path, timezone_offset=7):
    # Load the CSV data into a dictionary for quick lookup
    timestamp_pm10_mapping = {}
    with open(csv_file_path, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # Parse the timestamp and adjust for timezone
            now_timestamp = datetime.fromisoformat(row['Now Timestamp'])
            now_timestamp += timedelta(hours=timezone_offset)
            formatted_timestamp = now_timestamp.strftime('%Y%m%d_%H%M')
            formatted_timestamp += "00"
            timestamp_pm10_mapping[formatted_timestamp] = row['PM10']

    # Arrays to store the matched images and pm10 values
    x = []
    y = []

    # Iterate over all images in the folder
    for image_file in os.listdir(images_folder_path):
        if image_file.endswith(('.png', '.jpg', '.jpeg')):  # Add or remove file extensions as needed
            image_path = os.path.join(images_folder_path, image_file)
            image_timestamp = image_file.split('.')[0]
            
            # Match the image timestamp with the CSV data
            if image_timestamp in timestamp_pm10_mapping:
                pm10_value = timestamp_pm10_mapping[image_timestamp]
                y.append(pm10_value)
                # Load the image and append to x
                image = Image.open(image_path)
                image_rotated = image.rotate(-90, expand=True)
                image_resized = image_rotated.resize((227, 227))
                x.append(image_resized)
                print(f"Matched {image_file} with pm10 value: {pm10_value}")
            else:
                print(f"No match found for {image_file}")

    return x, y

download_file_from_gcs('sky-image', 'air_quality_data.csv', 'air_quality_data.csv')
x, y = match_images_with_csv('air_quality_data.csv', 'image')
display_random_images(x, y)
