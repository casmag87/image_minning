import unittest
from run import *
import hashlib

class test(unittest.TestCase):

    def test_build_url(self):
    
        token= "a129dd575c9fd980529650260bfb9078"
        x = 12.486632519760052
        y= 55.651260792
    
        expected ="https://api.dataforsyningen.dk/skraafoto_api/v1.0/collections/skraafotos2021/items?limit=12&bbox=12.486632519760052,55.651260792,12.486632519760052,55.651260792&token=a129dd575c9fd980529650260bfb9078"
        actual = url_build(x,y,token)
        
        url1 = hashlib.md5(str(actual).encode("utf-8")).hexdigest()
        url2 = hashlib.md5(str(expected).encode("utf-8")).hexdigest()
        
        self.assertEqual(actual, expected)
        
        self.assertEqual(url1, url2)

    def test_calculate_pixel_value(self):
        # Test data
        direction = 'west'
        data = {
            'west': {
                'f_mm': 146,
                'pixel_size': 0.00367,
                'sensor_cols': 14192,
                'sensor_rows': 10640,
                'ppo_x': 00,
                'ppo_y': 00
            }
        }

        # Expected output
        expected_f = 39782.01634877384
        expected_x0 = 7096.0
        expected_y0 = 5320.0

        # Call the function and check the output
        f, x0, y0 = calculate_pixel_value(direction, data)
        print(f,x0,y0)
        self.assertEqual(f, expected_f)
        self.assertEqual(x0, expected_x0)
        self.assertEqual(y0, expected_y0)


    def test_calc_(self):

        url = "https://api.dataforsyningen.dk/skraafoto_api/v1.0/collections/skraafotos2021/items?limit=12&bbox=12.486632519760052,55.651260792,12.486632519760052,55.651260792&token=a129dd575c9fd980529650260bfb9078"

        json_object = get_json_response(url)

        images = calc_for_directions(json_object)

        
        for image in images:
            assert image['xa'] <15000 and isinstance(image['xa'], float)
            f"number less than 15000 expected, got: {image['xa']}" 
            
            assert image['ya'] <15000 and isinstance(image['xa'], float)
            f"number less than 15000 expected, got: {image['ya']}" 
            
            assert image['xa'] >0 and isinstance(image['ya'], float) 
            f"number less than 15000 expected, got: {image['xa']}" 
            
            assert image['ya'] >0 and isinstance(image['ya'], float) 
            f"number less than 15000 expected, got: {image['ya']}" 


if __name__ == '__main__':
     unittest.main()
