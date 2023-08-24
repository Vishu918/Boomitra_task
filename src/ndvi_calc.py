import numpy as np
from logger_module import logger

class CalcForNdvi:
    """
    A class to calculate NDVI (Normalized Difference Vegetation Index) and its statistics.

    Attributes:
        ndvi_max (float): Maximum NDVI value.
        ndvi_min (float): Minimum NDVI value.
        ndvi_mean (float): Mean NDVI value.
        ndvi (numpy.ndarray): NDVI array.

    """
    def __init__(self):
        self.ndvi_max = None
        self.ndvi_min = None
        self.ndvi_mean = None
        self.ndvi = None

    def calculate_ndvi(self, nir, red):
        """
        Calculate NDVI (Normalized Difference Vegetation Index).

        Parameters:
            nir (numpy.ndarray): Near Infrared band array.
            red (numpy.ndarray): Red band array.
        """
        # Calculate NDVI, handling division by zero
        with np.errstate(divide='ignore', invalid='ignore'):
            self.ndvi = (nir - red) / (nir + red)
        logger.info("NDVI calculated")

        # Calculate statistics
        self.calculate_statistics()

    def calculate_statistics(self):
        """
        Calculate statistics of the NDVI array.
        """
        self.ndvi_mean = np.nanmean(self.ndvi)
        self.ndvi_min = np.nanmin(self.ndvi)
        self.ndvi_max = np.nanmax(self.ndvi)
        logger.info("NDVI statistics calculated")
