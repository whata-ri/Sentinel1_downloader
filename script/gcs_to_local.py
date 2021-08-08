import os

from google.cloud import storage as gcs
from google.oauth2 import service_account

key_path = "config/google/grasp-earth-report-service-account.json"
project_id = "grasp-earth-report-322308"
bucket_name = "grasp-earth-report-taiwan-dam"
download_dir = "data/taiwan_dam"

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