import requests
from PIL import Image
import numpy as np
import os
import sys
from flask import Flask

import tensorflow as tf
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))

ENDPOINT_URL = "http://127.0.0.1:5000/infer"

classes = { 1:'Speed limit (20km/h)',
            2:'Speed limit (30km/h)',
            3:'Speed limit (50km/h)',
            4:'Speed limit (60km/h)',
            5:'Speed limit (70km/h)',
            6:'Speed limit (80km/h)',
            7:'End of speed limit (80km/h)',
            8:'Speed limit (100km/h)',
            9:'Speed limit (120km/h)',
           10:'No passing',
           11:'No passing veh over 3.5 tons',
           12:'Right-of-way at intersection',
           13:'Priority road',
           14:'Yield',
           15:'Stop',
           16:'No vehicles',
           17:'Veh > 3.5 tons prohibited',
           18:'No entry',
           19:'General caution',
           20:'Dangerous curve left',
           21:'Dangerous curve right',
           22:'Double curve',
           23:'Bumpy road',
           24:'Slippery road',
           25:'Road narrows on the right',
           26:'Road work',
           27:'Traffic signals',
           28:'Pedestrians',
           29:'Children crossing',
           30:'Bicycles crossing',
           31:'Beware of ice/snow',
           32:'Wild animals crossing',
           33:'End speed + passing limits',
           34:'Turn right ahead',
           35:'Turn left ahead',
           36:'Ahead only',
           37:'Go straight or right',
           38:'Go straight or left',
           39:'Keep right',
           40:'Keep left',
           41:'Roundabout mandatory',
           42:'End of no passing',
           43:'End no passing veh > 3.5 tons' }

client = Flask(__name__)

model_path = "weights/Trafic_signs_model.h5"
model = tf.keras.models.load_model(model_path)

def predict():

    image = Image.open('resources/00094.png')
    image = image.resize((30, 30))
    image = np.asarray(image).astype(np.float32)
    img = np.expand_dims(image, axis=0)
    pred = model.predict(img)
    score = tf.nn.softmax(pred[0])
    cls = classes[np.argmax(score)]
    #prob = 100 * np.max(score)

    data = {'Class': cls}
    requests.post(ENDPOINT_URL, json=data)
    print(cls)
    return cls

def infer():
    client.run(host='0.0.0.0', port=5000, debug=True)
    return predict()

@client.route('/',methods=['GET','POST'])
def upload():
    return predict()

if __name__ =="__main__":
    infer()

