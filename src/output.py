import os.path
import matplotlib.pyplot as plt
import pandas as pd
from logger_module import logger

class OutputData:
    """
    A class to handle generation and storage of output. 

    Attributes:
        None
    """
    def __init__(self):
        pass

    def output_png_data(self, ndvi):
        """
        Generate and save NDVI PNG image.

        Parameters:
            ndvi (numpy.ndarray): NDVI array    
        """
        logger.info("Generating NDVI PNG image")
        plt.imshow(ndvi, cmap='RdYlGn')
        plt.colorbar(label='NDVI')
        output_folder = '../output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        plt.savefig(os.path.join(output_folder, 'ndvi_image.png'))
        plt.close()
        logger.info("NDVI PNG image saved")

    def output_csv_data(self, ndvi_mean, ndvi_min, ndvi_max):
        """
        Generate and save NDVI statistics as CSV. 

        Parameters:
            ndvi_mean (float): Mean NDVI value.
            ndvi_min (float): Minimum NDVI value.
            ndvi_max (float): Maximum NDVI value.
        """
        logger.info("Generating NDVI statistics CSV")
        parameters = ["mean_ndvi", "minimum_ndvi", "maximum_ndvi"]
        values = [ndvi_mean, ndvi_min, ndvi_max]
        ndvi_params_dict = {'parameters': parameters, 'value': values}
        ndvi_params_df = pd.DataFrame(ndvi_params_dict)
        output_folder = '../output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        ndvi_params_df.to_csv(os.path.join(output_folder, 'output.csv'), index=False)
        logger.info("NDVI statistics CSV saved")
