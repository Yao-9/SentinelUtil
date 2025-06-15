import ee
import time
from model import Coor;

class SentinelDownloader:
    def __init__(self, coors: list[Coor], path_prefix):
        self.coors = coors
        self.path_prefix = path_prefix

        ee.Authenticate()
        ee.Initialize(project='pacific-chalice-461523-j4')
    
    def download(self):
        for idx, coor in enumerate(self.coors):
            point = ee.Geometry.Point([coor.long, coor.lat])

            # Load Sentinel-2 image collection
            image = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                    .filterBounds(point)
                    .filterDate("2024-01-01", "2024-12-31")
                    .sort('CLOUDY_PIXEL_PERCENTAGE')
                    .first()
                    .select(['B4', 'B3', 'B2'])
                    .toUint16())
                
            task = ee.batch.Export.image.toCloudStorage(
                image=image,
                bucket='bucket_openaitozchallenge',
                description='sentinel_image',
                fileNamePrefix=f'sentinal_least_cloud/{self.path_prefix}/{idx}',
                scale=10,
                region=point.buffer(2000).bounds(),  # 500 meters buffer
                fileFormat='GeoTIFF'
            )
            task.start()
            print(f"task {idx} started")
            time.sleep(1)
            