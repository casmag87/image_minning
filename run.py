import requests
import math
import numpy 
from functools import reduce
from operator import add
from rasterio.plot import show
import rasterio
from rasterio.windows import Window
import time
from functools import reduce
from operator import getitem
import psycopg2
import re

def url_build(x,y,token):
   return f"https://api.dataforsyningen.dk/skraafoto_api/v1.0/collections/skraafotos2021/items?limit=12&bbox={x},{y},{x},{y}&token={token}"


def get_json_response(url: str):
   
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
    except requests.exceptions.HTTPError as err: 
        raise SystemExit(err)

    return response.json()




def create_image_dict(xa,ya,direction,props_link):
    return {'xa': xa, 'ya': ya, 'direction': direction, 'link': props_link} 


def extract_unique_directions(json_obj) -> dict:
    features = json_obj["features"]
    data = {}

    for item in features:
        properties = item['properties']
        direction = properties["direction"]
        if direction not in data:
            camera = {
                'm11': properties["pers:rotation_matrix"][0],
                'm12': properties["pers:rotation_matrix"][1],
                'm13':properties["pers:rotation_matrix"][2],
                'm21': properties["pers:rotation_matrix"][3],
                'm22': properties["pers:rotation_matrix"][4],
                'm23': properties["pers:rotation_matrix"][5],
                'm31': properties["pers:rotation_matrix"][6],
                'm32': properties["pers:rotation_matrix"][7],
                'm33': properties["pers:rotation_matrix"][8],
                "Xc": properties["pers:perspective_center"][0],
                "Yc": properties["pers:perspective_center"][1],
                "Zc": properties["pers:perspective_center"][2],
                "f_mm": properties["pers:interior_orientation"]["focal_length"],
                "ppo_x": properties["pers:interior_orientation"]["principal_point_offset"][0],
                "ppo_y": properties["pers:interior_orientation"]["principal_point_offset"][1],
                "pixel_size": properties["pers:interior_orientation"]["pixel_spacing"][0],
                "sensor_cols":properties["pers:interior_orientation"]["sensor_array_dimensions"][0],
                "sensor_rows":properties["pers:interior_orientation"]["sensor_array_dimensions"][1],
                "link":properties['asset:data']
            }
            data = {**data, direction: camera}

    return data


def calc_for_directions(json_obj) -> list:
    images = []
    data = extract_unique_directions(json_obj)
    
    for direction, props in data.items():
        link = data[direction]['link']
        X,Y,Z = 720392.1445558893,6173378.193170075,5.5
      
  
        
        xa, ya = photogrammetric_form(X, Y, Z, direction, data)
        image = {}
        image['xa'] = xa
        image['ya'] = ya
        image['direction'] = direction
        image['link'] = link
      
        images.append(image)
    return images

def calculate_pixel_value(direction, data):
    f = data[direction]['f_mm'] / data[direction]['pixel_size']
    x0 = data[direction]['sensor_cols'] * 0.5 + data[direction]['ppo_x'] / data[direction]['pixel_size']
    y0 = data[direction]['sensor_rows'] * 0.5 + data[direction]['ppo_y'] / data[direction]['pixel_size']
    return f,x0,y0

def photogrammetric_form(X:float, Y:float, Z:float,direction, data):
    f, x0, y0 = calculate_pixel_value(direction,data)
    dX = X-data[direction]['Xc']

    dY = Y-data[direction]['Yc']

    dZ = Z-data[direction]['Zc']
    n = (data[direction]['m31'] * dX +data[direction]['m32'] * dY + data[direction]['m33'] * dZ)

    xa = x0 - f * (data[direction]['m11'] * dX + data[direction]['m12'] * dY + data[direction]['m13'] * dZ) / n

    ya = y0 - f * (data[direction]['m21'] * dX + data[direction]['m22'] * dY +data[direction]['m23'] * dZ) / n
    return xa,ya

def crop_image(url:str):
    
    
    json_obj = get_json_response(url)

    images = calc_for_directions(json_obj)

    
    for image in images:
        
        with rasterio.open(image['link']) as src:
            if src is None:    
               return '%s unable to open'% image['link']
           
          
            xsize, ysize = 512, 512
            
           
            #xa,ya = lat_lon_to_xy(X,Y,Z,json_object)
            print("xa",image['xa'],image['ya'])
            print(image['direction'])
            

            if image['direction'] in ('nadir','south','north'): 
               xoff, yoff = image['xa']-xsize/2, src.shape[0]-image['ya'] -ysize/2

            if image['direction'] in ('west','east'):
              
                xoff,yoff = image['xa']-xsize/2, src.shape[0]-image['ya'] -ysize/2
                  
            window = Window(xoff, yoff, xsize, ysize)
            transform = src.window_transform(window)
        

            profile = src.meta.copy()
            profile.update({
            "driver": "GTiff",
            'height': ysize,
            'width': xsize,
            'transform': transform,
            'crs': 25832
                })
            
           
            with rasterio.open('image_'+str(image['direction'])+'.tif', 'w', **profile) as dst:
                dst.write(src.read(window=window))


def main():
    token= "a129dd575c9fd980529650260bfb9078"
    x = 12.5035067
    y = 55.65615644
    url = url_build(x,y,token)
    print(url)
    crop_image(url)








if __name__ == '__main__':
    main()
