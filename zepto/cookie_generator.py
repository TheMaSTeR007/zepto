import json
import requests
import pandas as pd

pincode_list = pd.read_excel(r'C:\Users\jaimin.gurjar\Downloads\qc_pincode.xlsx', sheet_name='Sheet1')['pincode']


def cookie_gen():
    cookie_list = list()
    for pincode in pincode_list:
        params = {
            'place_name': f'{pincode}',
        }

        pincode_response = requests.get('https://api.zepto.co.in/api/v1/maps/place/autocomplete/', params=params)
        dic = json.loads(pincode_response.text)
        place_id = dic['predictions'][0]['place_id']

        place_id_params = {
            'place_id': place_id
        }

        place_id_response = requests.get('https://api.zepto.co.in/api/v1/maps/place/details/', params=place_id_params)

        dic_2 = json.loads(place_id_response.text)
        latitude = dic_2['result']['geometry']['location']['lat']
        longitute = dic_2['result']['geometry']['location']['lng']
        out_dict = {
            "cookie_dict": {
                'latitude': f"{latitude}",
                'longitude': f"{longitute}"},
            "pincode": f"{pincode}"
        }
        cookie_list.append(out_dict)
        print('generating...')
    with open('cookies_json.json', 'w') as file:
        file.write(json.dumps(cookie_list))
    print('Cookies generated !!')


cookie_gen()
