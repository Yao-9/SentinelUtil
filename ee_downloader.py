import ee
import time
from model import Coor;

class SentinelDownloader:
    def __init__(self, coors: list[Coor], path_prefix):
        self.coors = coors
        self.path_prefix = path_prefix

        ee.Authenticate()
        ee.Initialize(project='pacific-chalice-461523-j4')

    def mask_clouds(self, image_pair):
        s2_img = ee.Image(image_pair.get('primary'))
        cloud_img = ee.Image(image_pair.get('secondary'))
        
        cloud_prob = cloud_img.select('probability')
        is_clear = cloud_prob.lt(40)  # Change 40 to your threshold
    
        return s2_img.updateMask(is_clear).copyProperties(s2_img, ['system:time_start'])
    
    def download(self):
        for idx, coor in enumerate(self.coors):
            # Define location (lat, lon)
            point = ee.Geometry.Point([coor.long, coor.lat])

            # Load Sentinel-2 image collection
            image = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
                    .filterBounds(point)
                    .filterDate("2024-01-01", "2024-12-31")
                    .sort('CLOUDY_PIXEL_PERCENTAGE')
                    .first()
                    .select(['B4', 'B3', 'B2'])
                    .toUint16())
            
            # cloud_prob = (ee.ImageCollection("COPERNICUS/S2_CLOUD_PROBABILITY") 
            #         .filterBounds(point) 
            #         .filterDate("2024-01-01", "2024-01-31"))
            
            # joined_image = ee.Join.inner().apply(
            #     primary=image,
            #     secondary=cloud_prob,
            #     condition=ee.Filter.equals(leftField='system:index', rightField='system:index')
            # )

            # masked_collection = ee.ImageCollection(joined_image.map(self.mask_clouds))
            # composite = masked_collection.median().select(['B4', 'B3', 'B2']).toUint16()
                        
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


            