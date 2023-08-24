import rasterio
import pandas as pd
import os.path
import matplotlib.pyplot as plt
class OutputData:
    def __int__(self):
        pass

    def output_png_data(self,  ndvi ):
        # # Save the masked NDVI to one tif per polygon
        # output_folder = r'output'
        # ndvi_path = f'ndvi_{feature["properties"]["Partner ID"]}.png'
        #
        # meta = nir_src.meta
        # # Don't forget to update the dtype! Your original code didn't, so the Int16 output truncated NDVI values to
        # # all 0's
        # meta.update({"driver": "GTiff", "dtype": ndvi.dtype, "height": window.height, "width": window.width,
        #              "transform": window_transform})
        # with rasterio.open(os.path.join(output_folder,ndvi_path), 'w', **meta) as dst:
        #     dst.write(ndvi)

        # Create PNG image of NDVI array
        plt.imshow(ndvi, cmap='RdYlGn')
        plt.colorbar(label='NDVI')
        plt.savefig('ndvi_image.png')
        plt.close()

    def output_csv_data(self, ndvi_mean,  ndvi_min , ndvi_max):
        parameter = ["mean_ndvi", "minimum_ndvi", "maximim_ndvi"]
        value = [ndvi_mean, ndvi_min , ndvi_max]
        ndvi_params_dict = {'parameters':parameter, 'value':value}
        ndvi_params_df = pd.DataFrame(ndvi_params_dict)
        output_folder = r'output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        ndvi_params_df.to_csv(os.path.join(output_folder,'output.csv'))



