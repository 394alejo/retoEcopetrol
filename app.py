# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 08:09:55 2019

@author: Diana Acosta
"""

#!flask/bin/python
import requests
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import render_template, redirect, url_for
#import pandas as pd
import cv2 as cv
import numpy as np

app = Flask(__name__)




@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/ecopetrol/api/v1.0/', methods=['GET'])
def get_hello():
    return  "<img src='static/fruit.jpg'/>"

@app.route('/gallery')
def get_gallery():
    #return "<img src='static/s.jpg'/>"
    return render_template("resultado.html")


@app.route("/")
def main():
    return render_template('index.html')

@app.route('/ecopetrol/api/v1.0/', methods=['POST'])
def detect_helment():
    if request.method == 'POST':
        endpoint = 'https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/21be4d2c-fa3a-4c44-ba22-2360b047742c/detect/iterations/cascos/image'
        print(request.files['file'])
        image = request.files['file'].read()
        nparr = np.fromstring(image, np.uint8)
        img_np = cv.imdecode(nparr, cv.IMREAD_COLOR)
        #image.save('C:/Users/Diana Acosta/OneDrive - Idata/Ecopetrol/Reto/asd.jpg')              
        headers = {
            'Prediction-Key': '177f19ca3b8448a5a3f8909315098d41',
            'Content-Type': 'application/octet-stream'
        }
        resp = requests.post(endpoint, data=image, headers=headers)
        resp = resp.json()        
        # imgHeight, imgWidth, channels = img_np.shape      
        imgWidth = img_np.shape[1] 
        imgHeight = img_np.shape[0]    
        
        for prediction in resp['predictions']:
        
            probabilidad = float(prediction['probability'])*100
            if probabilidad > 60:
                #print ("\t" + prediction['tagName'] + ": {0:.2f}%".format(prediction['probability'] * 100), prediction['boundingBox']['left'], prediction['boundingBox']['top'], prediction['boundingBox']['width'], prediction['boundingBox']['height'])
                left = int(prediction['boundingBox']['left']* imgWidth)
                top = int(prediction['boundingBox']['top']*imgHeight)
                width = int(left + (prediction['boundingBox']['width']*imgWidth))
                height = int(top + (prediction['boundingBox']['height']*imgHeight))
                frame = cv.rectangle(img_np, (left, top), (width,height), (0,255,255), 2)
                
                cv.imwrite('static/s.jpg',frame)
     
        #response = make_response(jsonify(resp, 200))
        return redirect(url_for('get_gallery'))
    else:
        response = make_response(
                jsonify({'error': 'Imagen no encontrada'}), 
                404)
    
        return response
        

if __name__ == '__main__':
    app.run(debug=True)
    
#
