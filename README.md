## Farm Field Health Monitoring using Satellite Data (NDVI Calculation)
This repository contains a Python workflow to help farmers monitor the health of their fields in adverse weather conditions using satellite data. The workflow calculates the Normalized Difference Vegetation Index (NDVI) based on Sentinel 2 Imagery. NDVI is a crucial indicator of plant health, allowing farmers to identify stressed areas in their fields and take necessary measures to ensure optimal yield.

## Table of Contents

- [Introduction](#introduction)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Setup](#setup)
- [Output](#output)
- [References](#references)
- [Contact](#contact)

## Introduction

Adverse weather conditions can pose a threat to crop yield, and it's essential for farmers to receive advanced warnings about stressed areas in their fields. This repository provides a Python-based solution to extract and process Sentinel 2 Imagery using remote sensing techniques. By calculating NDVI and generating NDVI images, this workflow helps farmers visualize the health status of different field regions.

## Getting Started
### Requirements

- Python 3.x
- Rasterio
- Geopandas
- Matplotlib
- Numpy


### Setup

1. Clone this repository:

```bash
git clone https://github.com/Vishu918/Boomitra_task.git
```

2. Change directory:

```bash
cd Boomitra_task
```
3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Run main script from src folder: 
```bash
cd src
```
```bash
python main.py
```
**Note**
>> main.py scrip takes 3 inputs two Sentinel 2 imagery and a json file which contains the Polygon
geometric object. You can give inputs of your choice by editing input.json in the "input" directory. [You can access input.json from here](input/input.json)

## Output

The script generates the following outputs:

1. NDVI Image: A PNG image representing the NDVI values of the selected field region.
2. Statistics: A text file or CSV file containing statistics (mean, min, max) of the NDVI image array.

Sample outputs can be found in the "output" directory.[You can access input.json from here](output)

**Note**
You can check logs from app.log file [You can access app.log from here](src/app.log)

## References

- [NDVI Calculation](https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index)
- [Rasterio Documentation](https://rasterio.readthedocs.io/en/latest/)
- [Geopandas Documentation](https://geopandas.org/)
- [Rasterstats Documentation](https://pythonhosted.org/rasterstats/)
- [Rioxarray Documentation](https://corteva.github.io/rioxarray/stable/)

## Contact

For any questions or assistance, please contact vmalwadkar21@gmail.com .