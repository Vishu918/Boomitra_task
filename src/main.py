from read_input import ReadingInputData
from ndvi_calc import CalcForNdvi
from output import OutputData
import json
import logging
read_inp_obj = ReadingInputData()
ndvi_calc_obj = CalcForNdvi()
output_obj = OutputData()


class HealthyVegetationArea:
    def __init__(self, nir_path, red_path, polygon_path):
        self.max_val = None
        self.min_val = None
        self.mean_val = None
        self.window_transform = None
        self.ndvi_array = None
        self.window = None
        self.nir_src = None
        self.poly_feature = None
        self.argument = None
        self.red = None
        self.nir = None
        self.nir_path = nir_path
        self.red_path = red_path
        self.polygon_path = polygon_path
        self.read_input_data()
        self.NDVI_calculations()
        self.store_output_data()

    def read_input_data(self):
        read_inp_obj.read_polygon_json(self.polygon_path)
        self.b = read_inp_obj.open_tif_data(self.nir_path, self.red_path)

    def NDVI_calculations(self):
        self.nir = read_inp_obj.nir
        self.red = read_inp_obj.red
        ndvi_calc_obj.calc(self.nir, self.red)

    def store_output_data(self):
        self.poly_feature = read_inp_obj.feature
        self.nir_src = read_inp_obj.nir_src
        self.window = read_inp_obj.window
        self.window_transform = read_inp_obj.window_transform
        self.ndvi_array = ndvi_calc_obj.ndvi
        self.mean_val = ndvi_calc_obj.ndvi_mean
        self.min_val = ndvi_calc_obj.ndvi_min
        self.max_val = ndvi_calc_obj.ndvi_max

        output_obj.output_png_data(self.poly_feature, self.nir_src, self.ndvi_array,
                                   self.window, self.window_transform)
        output_obj.output_csv_data(self.mean_val, self.min_val , self.max_val)


if __name__ == "__main__":
    with open('input/input.json') as inp_file:
        inp_data = json.load(inp_file)
    # Sentinel-2 bands
    sentinel_2_imagery_b1 = inp_data['sentinel_2_imagery_b1']
    sentinel_2_imagery_b2 = inp_data['sentinel_2_imagery_b2']
    json_file = inp_data['json_file']
    HealthyVegetationArea(sentinel_2_imagery_b1, sentinel_2_imagery_b2, json_file)
    logging.info("Task completed")
