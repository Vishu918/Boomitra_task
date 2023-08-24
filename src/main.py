from read_input import ReadingInputData
from ndvi_calc import CalcForNdvi
from output import OutputData
import json
from logger_module import logger

read_inp_obj = ReadingInputData()
ndvi_calc_obj = CalcForNdvi()
output_obj = OutputData()



class HealthyVegetationArea:
    """
    A class to process satellite data and calculate NDVI for healthy vegetation areas.

    Attributes:
        nir_path (str): Path to the Near Infrared (NIR) band image.
        red_path (str): Path to the Red band image.
        polygon_path (str): Path to the polygon GeoJSON file.
        max_val (float): Maximum NDVI value.
        min_val (float): Minimum NDVI value.
        mean_val (float): Mean NDVI value.
        red: Red band data.
        nir: NIR band data.
    """
    
    def __init__(self, nir_path, red_path, polygon_path):
        """
        Initialize the HealthyVegetationArea class.

        Parameters:
            nir_path (str): Path to NIR band image.
            red_path (str): Path to Red band image.
            polygon_path (str): Path to the polygon GeoJSON file.
        """
        self.max_val = None
        self.min_val = None
        self.mean_val = None
        self.ndvi_array = None
        self.red = None
        self.nir = None
        self.nir_path = nir_path
        self.red_path = red_path
        self.polygon_path = polygon_path
        self.read_input_data()
        self.NDVI_calculations()
        self.store_output_data()
        
    

    def read_input_data(self):
        """
        Read input data and preprocesses it.
        """
        logger.info('Reading input data...')
        read_inp_obj.read_polygon_json(self.polygon_path)
        read_inp_obj.open_tif_data(self.nir_path, self.red_path)
       
        
    def NDVI_calculations(self):
        """
        Perform NDVI calculations on the provided data.
        """
        logger.info('Performing NDVI calculations...')
        self.nir = read_inp_obj.subset_b8
        self.red = read_inp_obj.subset_b4
        ndvi_calc_obj.calculate_ndvi(self.nir, self.red)

    def store_output_data(self):
        """
        Store the calculated NDVI data and output results.
        """
        logger.info('Storing output data...')
        self.ndvi_array = ndvi_calc_obj.ndvi
        self.mean_val = ndvi_calc_obj.ndvi_mean
        self.min_val = ndvi_calc_obj.ndvi_min
        self.max_val = ndvi_calc_obj.ndvi_max

        output_obj.output_png_data(self.ndvi_array)
        output_obj.output_csv_data(self.mean_val, self.min_val , self.max_val)


if __name__ == "__main__":
    with open('../input/input.json') as inp_file:
        inp_data = json.load(inp_file)
    # Sentinel-2 bands
    sentinel_2_imagery_b1 = inp_data['sentinel_2_imagery_b1']
    sentinel_2_imagery_b2 = inp_data['sentinel_2_imagery_b2']
    # polygon data json file
    json_file = inp_data['json_file']
    HealthyVegetationArea(sentinel_2_imagery_b1, sentinel_2_imagery_b2, json_file)
    logger.info("Task Completed")
