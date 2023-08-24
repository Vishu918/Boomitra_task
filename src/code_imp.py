import rasterio
import geopandas as gpd
from rasterio.mask import mask
import matplotlib.pyplot as plt
import numpy as np

# Paths and URLs
sentinel_2_imagery_b8 = "s3://sentinel-cogs/sentinel-s2-l2a-cogs/36/N/YF/2023/6/S2B_36NYF_20230605_0_L2A/B08.tif" #nir
sentinel_2_imagery_b4 = "s3://sentinel-cogs/sentinel-s2-l2a-cogs/36/N/YF/2023/6/S2B_36NYF_20230605_0_L2A/B04.tif" #red
polygon_file = "sample_polygon.geojson"  # Replace with actual path

# Read Polygon using geopandas
polygon_gdf = gpd.read_file(polygon_file)

# Open Sentinel 2 imagery using rasterio
with rasterio.Env(AWS_NO_SIGN_REQUEST="YES"):
    with rasterio.open(sentinel_2_imagery_b8) as src_b8, rasterio.open(sentinel_2_imagery_b4) as src_b4:
        # Reproject polygon to match the imagery's projection
        polygon_gdf = polygon_gdf.to_crs("EPSG:32636")

        # Create a mask indicating where the polygon overlaps with the imagery
        polygon_mask = [geom for geom in polygon_gdf.geometry]

        # Read only the subset of the imagery that overlaps with the polygon
        subset_b8, subset_transform_b8 = mask(src_b8, polygon_mask, crop=True)
        subset_b4, subset_transform_b4 = mask(src_b4, polygon_mask, crop=True)

        # Remove the extra dimension
        subset_b8 = subset_b8.squeeze()
        subset_b4 = subset_b4.squeeze()

        # Calculate NDVI
        ndvi = (subset_b8 - subset_b4) / (subset_b8 + subset_b4)

# Calculate statistics
ndvi_mean = np.nanmean(ndvi)
ndvi_min = np.nanmin(ndvi)
ndvi_max = np.nanmax(ndvi)

# Create PNG image of NDVI array
plt.imshow(ndvi, cmap='RdYlGn')
plt.colorbar(label='NDVI')
plt.savefig('ndvi_image.png')
plt.close()

# Save statistics to a text file
with open('ndvi_stats.txt', 'w') as f:
    f.write(f"NDVI Mean: {ndvi_mean}\n")
    f.write(f"NDVI Min: {ndvi_min}\n")
    f.write(f"NDVI Max: {ndvi_max}\n")
