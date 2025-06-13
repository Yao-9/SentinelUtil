# import rasterio
# from rasterio.plot import show
# import matplotlib.pyplot as plt
# import numpy as np

# with rasterio.open("/Users/yaozhao/Downloads/test_sentinal2_1.tif") as src:
#     img = src.read([1, 2, 3])  # R, G, B bands
#     # Transpose to HWC format for matplotlib (bands, rows, cols) -> (rows, cols, bands)
#     # img = np.transpose(img, (1, 2, 0))
#     print(img)

#     plt.figure(figsize=(8, 8))
#     plt.imshow(img)
#     plt.title("Sentinel-2 True Color (B4-B3-B2)")
#     plt.axis('off')
#     plt.show()
import rasterio
import numpy as np
import matplotlib.pyplot as plt

def open_gee_rgb_geotiff(filepath):
    with rasterio.open(filepath) as src:
        print(src)
        # Read bands in order: Red (B4), Green (B3), Blue (B2)
        red = src.read(1).astype(np.float32)
        green = src.read(2).astype(np.float32)
        blue = src.read(3).astype(np.float32)

        # # Normalize reflectance from [0, 10000] to [0, 1]
        red /= 10000.0
        green /= 10000.0
        blue /= 10000.0

        # Stack and clip to [0, 1]
        rgb = np.stack([red, green, blue], axis=-1)
        rgb = np.clip(rgb, 0, 1)

        return rgb

# Load the image
file_path = "/Users/yaozhao/Downloads/sentinal_positive_1.tif"  # Replace with your actual path
rgb_image = open_gee_rgb_geotiff(file_path)

# Display it
plt.figure(figsize=(10, 10))
plt.imshow(rgb_image)
print(rgb_image)
plt.title("True Color Image (B4-B3-B2)")
plt.axis('off')
plt.show()