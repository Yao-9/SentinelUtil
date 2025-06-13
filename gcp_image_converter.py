from google.cloud import storage
from image_converter import geotiff_to_jpg

client = storage.Client()
bucket = client.bucket('bucket_openaitozchallenge')
blobs = bucket.list_blobs(prefix='sentinal_least_cloud/positive')

for idx, blob in enumerate(blobs):
    content = blob.download_as_bytes()
    geotiff_to_jpg(content, f"output/{idx}.jpg")
