import rasterio
import geopandas as gpd
from rasterio.mask import mask
from logger_module import logger

class ReadingInputData:
    """
    A class to handle reading and processing input data for NDVI calculation.

    Attributes:
        None
    """
    def __init__(self):
        self.polygon_mask = None
        self.subset_transform_b4 = None
        self.subset_transform_b8 = None
        self.subset_b4 = None
        self.subset_b8 = None
        self.nir_src = None
        self.red_src = None
        self.polygon_gdf = None

    def read_polygon_json(self, polygon_path):
        """
        Read the polygon GeoJSON file and reproject it to match the imagery's projection.
        """
        self.polygon_gdf = gpd.read_file(polygon_path)
        self.polygon_gdf = self.polygon_gdf.to_crs("EPSG:32636")
        logger.info("Polygon read and reprojected")

    def open_tif_data(self, nir_path, red_pth):
        """
        Open the AWS COG datasets for NIR and Red bands.
        Extract subsets of the imagery that overlap with the polygon.
        """
        with rasterio.Env(AWS_NO_SIGN_REQUEST="YES"):
            with rasterio.open(nir_path) as nir_src, rasterio.open(red_pth) as red_src:
                self.nir_src = nir_src
                self.red_src = red_src
                self.polygon_mask = [geom for geom in self.polygon_gdf.geometry]
                self.subset_b8, self.subset_transform_b8 = mask(self.nir_src, self.polygon_mask, crop=True)
                self.subset_b4, self.subset_transform_b4 = mask(self.red_src, self.polygon_mask, crop=True)
                self.subset_b8 = self.subset_b8.squeeze()
                self.subset_b4 = self.subset_b4.squeeze()
                logger.info("TIF data opened and subsets extracted")

