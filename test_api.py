# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 09:02:17 2019

@author: Diana Acosta

"""
import requests
import cv2 as cv

##### Test API

url = 'http://127.0.0.1:5000/ecopetrol/api/v1.0/'

f = open('C:/Users/Diana Acosta/Downloads/cascos/140.jpg', 'rb')

response = requests.post(url, files={'image': f})
#response2 = json.dumps(response)

f.close()

            