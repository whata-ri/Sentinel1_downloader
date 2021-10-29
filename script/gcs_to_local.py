import os

from google.cloud import storage as gcs
from google.oauth2 import service_account

key_path = "config/google/sentinel-datahub-service-account.json"
project_id = "sentinel-datahub"
bucket_name = "ge-los-angeles"
download_dir = "data/los_angeles"

os.makedirs(download_dir, exist_ok=True)

credential = service_account.Credentials.from_service_account_file(key_path)
client = gcs.Client(project_id, credentials=credential)
bucket = client.get_bucket(bucket_name)

flist = [file.name for file in client.list_blobs(bucket_name)]

for fname in flist:
    blob = bucket.blob(fname)
    blob.download_to_filename(
        os.path.join(download_dir, fname)
    )
    print(f"download: {fname}")
