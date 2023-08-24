import rasterio
import geopandas as gpd
from rasterio.windows import transform
from rasterio.features import geometry_window, geometry_mask
from rasterio.mask import mask

class ReadingInputData:
    def __init__(self):
        self.polygon_mask = None
        self.subset_transform_b4 = None
        self.subset_transform_b8 = None
        self.subset_b4 = None
        self.subset_b8 = None
        self.feature = None
        self.red = None
        self.nir = None
        self.window_shape = None
        self.window = None
        self.window_transform = None
        self.red_src = None
        self.nir_src = None
        self.polygon_gdf = None

    def read_polygon_json(self, polygon_path):
        self.polygon_gdf = gpd.read_file(polygon_path)
        self.polygon_gdf = self.polygon_gdf.to_crs("EPSG:32636")

    def open_tif_data(self, nir_path, red_pth):
        # Open the AWS COG datasets
        with rasterio.Env(AWS_NO_SIGN_REQUEST="YES"):
            with rasterio.open(nir_path) as nir_src, rasterio.open(red_pth) as red_pth:
                # Create a mask indicating where the polygon overlaps with the imagery
                self.nir_src = nir_src
                self.red_src = red_pth
                # Create a mask indicating where the polygon overlaps with the imagery
                self.polygon_mask = [geom for geom in self.polygon_gdf.geometry]
                # Read only the subset of the imagery that overlaps with the polygon
                self.subset_b8, self.subset_transform_b8 = mask(self.nir_src, self.polygon_mask, crop=True)
                self.subset_b4, self.subset_transform_b4 = mask(self.red_src, self.polygon_mask, crop=True)
                # Remove the extra dimension
                self.subset_b8 = self.subset_b8.squeeze()
                self.subset_b4 = self.subset_b4.squeeze()


                # for feature in self.polygon_gdf.iterfeatures(show_bbox=True):
                #     self.feature = feature
                #     # Get a window
                #     self.window = geometry_window(self.nir_src, [feature["geometry"]])
                #     self.window_transform = transform(self.window, self.nir_src.transform)
                #     self.window_shape = (self.window.height, self.window.width)
                #
                #     # Read all the data in the window, masking out any NoData
                #     self.nir = self.nir_src.read(window=self.window, masked=True).astype('float32')
                #     self.red = self.red_src.read(window=self.window, masked=True).astype('float32')
                #
                #     # Update the NoData mask to exclude anything outside the polygon
                #     mask = geometry_mask([feature["geometry"]], self.window_shape, self.window_transform)
                #     self.nir.mask += mask
                #     self.red.mask += mask
