import os

import urllib.request

 

url_dict = {

    "attractors": 'https://www.dropbox.com/scl/fi/v1sab0qvuq2wy1vo537ke/attfiles.zip?rlkey=b1whu3huozsbamyug2d7txphm&dl=1'

}

 

def main():

    data_name = 'attractors'
    data_path = "./attfiles.zip"
    data_url = url_dict["attractors"]
    
    urllib.request.urlretrieve(data_url, data_path)

    print(f"{data_name} data has been downloaded and saved in {data_path}")


 

if __name__ == '__main__':

    main()