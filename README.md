# Aerial Imagery Cropper using Dataforsyningen API

This Python script uses the Dataforsyningen.dk Skraafoto API to fetch metadata and imagery from aerial photographs, calculate perspective projection coordinates, and crop image tiles using rasterio.

## Features

- Builds API queries to Dataforsyningen's `skraafoto` endpoint
- Extracts photogrammetric metadata from JSON
- Calculates image coordinates (xa, ya) using perspective formulas
- Supports directional filtering (north, south, west, east, nadir)
- Crops and writes `.tif` image tiles based on calculated positions
- Handles raster data using `rasterio`

## Requirements

Install the dependencies using pip:

```bash
pip install requests rasterio numpy psycopg2
