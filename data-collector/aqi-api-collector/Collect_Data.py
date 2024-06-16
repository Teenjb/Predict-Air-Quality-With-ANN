import re
from google.cloud import storage
from datetime import datetime, timedelta

def get_closest_file_name(bucket, prefix, target_datetime):
    """
    Gets the closest file name to the target datetime.
    """
    # List all files in the bucket with the given prefix
    blobs = list(bucket.list_blobs(prefix=prefix))
    # Filter out files that match the date format using regex
    regex = re.compile(r'\d{8}_\d{6}')
    filtered_blobs = [blob for blob in blobs if regex.match(blob.name)]

    # Find the closest file name to the target datetime
    closest_blob = None
    min_diff = timedelta.max
    for blob in filtered_blobs:
        # Extract the datetime from the file name
        file_datetime = datetime.strptime(blob.name, '%Y%m%d_%H%M%S.jpg')
        diff = abs(target_datetime - file_datetime)
        if diff < min_diff:
            min_diff = diff
            closest_blob = blob
    return closest_blob

def download_files_in_interval(bucket_name, start_date, end_date, service_account_path, interval_minutes=30):
    """
    Downloads files from Google Cloud Storage that are within the specified datetime interval.
    """
    # Authenticate using the service account
    storage_client = storage.Client.from_service_account_json(service_account_path)

    # Convert string dates to datetime objects
    start_datetime = datetime.strptime(start_date, '%Y%m%d_%H%M%S')
    end_datetime = datetime.strptime(end_date, '%Y%m%d_%H%M%S')

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Calculate the number of intervals
    current_datetime = start_datetime
    while current_datetime <= end_datetime:
        # Set daily start and end times
        daily_start = current_datetime.replace(hour=7, minute=0, second=0)
        daily_end = current_datetime.replace(hour=18, minute=30, second=0)

        # Skip times outside of 7am-6:30pm
        if daily_start <= current_datetime <= daily_end:
            prefix = current_datetime.strftime('%Y%m%d_')
            # Find the closest file
            closest_blob = get_closest_file_name(bucket, prefix, current_datetime)
            if closest_blob:
                new_file_name = current_datetime.strftime('%Y%m%d_%H%M%S.jpg')  # Assuming the file is a .jpg
                destination_file_name = f"image/{new_file_name}"  # Replace 'local/path/to/' with your local directory
                
                # Download the blob to a local file
                closest_blob.download_to_filename(destination_file_name)
                print(f"Downloaded and renamed {closest_blob.name} to {new_file_name}.")
            else:
                print(f"No file found close to {current_datetime.strftime('%Y%m%d_%H%M%S')}.")
        
        # Increment the current time by the interval
        current_datetime += timedelta(minutes=interval_minutes)
        # If the current time is past 6:30pm, skip to the next day's 7am
        if current_datetime > daily_end:
            current_datetime = (current_datetime + timedelta(days=1)).replace(hour=7, minute=0, second=0)

download_files_in_interval('sky-image', '20240526_070000', '20240603_180000', 'ai-finpro-data-labeling-key.json')
