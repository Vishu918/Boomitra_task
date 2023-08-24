import rasterio
import geopandas as gpd
from rasterio.windows import transform
from rasterio.features import geometry_window, geometry_mask


class ReadingInputData:
    def __init__(self):
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
        print(type(self.polygon_gdf))

    def open_tif_data(self, nir_path, red_pth):
        # Open the AWS COG datasets
        with rasterio.Env(AWS_NO_SIGN_REQUEST="YES"):
            with rasterio.open(nir_path) as nir_src, rasterio.open(red_pth) as red_pth:
                self.nir_src = nir_src
                self.red_src = red_pth
                for feature in self.polygon_gdf.iterfeatures(show_bbox=True):
                    self.feature = feature
                    # Get a window
                    self.window = geometry_window(self.nir_src, [feature["geometry"]])
                    self.window_transform = transform(self.window, self.nir_src.transform)
                    self.window_shape = (self.window.height, self.window.width)

                    # Read all the data in the window, masking out any NoData
                    self.nir = self.nir_src.read(window=self.window, masked=True).astype('float32')
                    self.red = self.red_src.read(window=self.window, masked=True).astype('float32')

                    # Update the NoData mask to exclude anything outside the polygon
                    mask = geometry_mask([feature["geometry"]], self.window_shape, self.window_transform)
                    self.nir.mask += mask
                    self.red.mask += mask



