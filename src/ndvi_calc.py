import rasterio
import geopandas as gpd
from rasterio.windows import transform
from rasterio.features import geometry_window, geometry_mask


class CalcForNdvi:
    def __init__(self):
        self.ndvi_max = None
        self.ndvi_min = None
        self.ndvi_mean = None
        self.ndvi = None

    def __int__(self):
        pass
        # Calculate NDVI

    def calc(self, nir, red):
        self.ndvi = (nir - red) / (nir + red)
        self.ndvi_mean = self.ndvi.mean()
        self.ndvi_min = self.ndvi.min()
        self.ndvi_max = self.ndvi.max()
        print(self.ndvi_mean, self.ndvi_min, self.ndvi_max)
        print(self.ndvi)



