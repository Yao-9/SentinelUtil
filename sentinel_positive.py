from ee_downloader import SentinelDownloader
import pandas as pd
from io import StringIO
from google.cloud import storage
from model import Coor

# Initialize a client
client = storage.Client(project="pacific-chalice-461523-j4")

# Define bucket and file names
bucket_name = "bucket_openaitozchallenge"
source_blob_name = "amazon_dataset.csv"  # GCS path

# Get the bucket
bucket = client.bucket(bucket_name)

# Get the blob (file) from the bucket
blob = bucket.blob(source_blob_name)

# Download the file to local filesystem
contents = blob.download_as_text()

df = pd.read_csv(StringIO(contents))

coors = []

for _, record in df.iterrows():
    coors.append(Coor(lat=record["Latitude"], long=record["Longitude"]))

downloader = SentinelDownloader(coors, 'positive')
downloader.download()
