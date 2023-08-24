

import rasterio
import geopandas as gpd
from rasterio.windows import transform
from rasterio.features import geometry_window, geometry_mask

# Sentinel-2 bands
nir_path = 's3://sentinel-cogs/sentinel-s2-l2a-cogs/36/N/YF/2023/6/S2B_36NYF_20230605_0_L2A/B08.tif'
red_path = 's3://sentinel-cogs/sentinel-s2-l2a-cogs/36/N/YF/2023/6/S2B_36NYF_20230605_0_L2A/B04.tif'

# Polygon path (the file contains 3 polygons with a unique ID field)
polygon_path = 'path_to_sample_polygon.geojson'
polygon_id_field = "ID"

# Load and transform the polygon
polygon_gdf = gpd.read_file(polygon_path)
polygon_gdf = polygon_gdf.to_crs("EPSG:32636")

# Open the AWS COG datasets
with rasterio.Env(AWS_NO_SIGN_REQUEST="YES"):
    with rasterio.open(nir_path) as nir_src, rasterio.open(red_path) as red_src:
        # loop through each feature in the GDF
        for feature in polygon_gdf.iterfeatures(show_bbox=True):
            # Get a window
            window = geometry_window(nir_src, [feature["geometry"]])
            window_transform = transform(window, nir_src.transform)
            window_shape = (window.height, window.width)

            # Read all the data in the window, masking out any NoData
            nir = nir_src.read(window=window, masked=True).astype('float32')
            red = red_src.read(window=window, masked=True).astype('float32')

            # Update the NoData mask to exclude anything outside the polygon
            mask = geometry_mask([feature["geometry"]], window_shape, window_transform)
            nir.mask += mask
            red.mask += mask

            # Calculate NDVI
            ndvi = (nir - red) / (nir + red)

            # Save the masked NDVI to one tif per polygon
            ndvi_path = f'ndvi_{feature["properties"][polygon_id_field]}.tif'

            meta = nir_src.meta
            # Don't forget to update the dtype! Your original code didn't, so the Int16 output truncated NDVI values to all 0's
            meta.update({"driver": "GTiff", "dtype": ndvi.dtype, "height": window.height, "width": window.width,
                         "transform": window_transform})
            with rasterio.open(ndvi_path, 'w', **meta) as dst:
                dst.write(ndvi)