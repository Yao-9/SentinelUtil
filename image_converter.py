import numpy as np
from PIL import Image
from rasterio.io import MemoryFile

def geotiff_to_jpg(geotiff_content, output_jpg_path):
    with MemoryFile(geotiff_content) as memfile:
        with memfile.open() as src:
            # Read B4 (Red), B3 (Green), B2 (Blue)
            red = src.read(1)  # Band 1: B4
            green = src.read(2)  # Band 2: B3
            blue = src.read(3)  # Band 3: B2

            # Stack to RGB array
            rgb = np.stack([red, green, blue], axis=-1)

            # Normalize to 0–255 (uint8)
            def normalize(band):
                band_min, band_max = band.min(), band.max()
                band_scaled = (band - band_min) / (band_max - band_min + 1e-6)  # avoid divide by zero
                return (band_scaled * 255).astype(np.uint8)

            rgb_normalized = np.stack([normalize(red), normalize(green), normalize(blue)], axis=-1)

            # Save as JPG
            img = Image.fromarray(rgb_normalized)
            img.save(output_jpg_path)
            print(f"Saved JPG to {output_jpg_path}")