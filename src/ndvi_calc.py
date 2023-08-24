import rasterio
import geopandas as gpd
from rasterio.windows import transform
from rasterio.features import geometry_window, geometry_mask
import numpy as np


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
        # Calculate NDVI, handling division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            self.ndvi = np.where((nir + red) == 0, 0, (nir - red) / (nir + red))
        self.ndvi_mean = self.ndvi.mean()
        self.ndvi_min = self.ndvi.min()
        self.ndvi_max = self.ndvi.max()
        print(f"HEREEE {self.ndvi_mean}{self.ndvi_min}{self.ndvi_max}")
        print(self.ndvi)



