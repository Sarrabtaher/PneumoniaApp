from flask import Flask, render_template, request
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import pandas as pd
import os
import matplotlib.image as mpimg
from tensorflow.keras.preprocessing.image import ImageDataGenerator 



app = Flask(__name__)


model = load_model('CNN_model150.h5')

model.make_predict_function()

def predict_label(img_path):
    
    img=image.load_img(img_path,target_size=(150,150),grayscale=True)
    x=image.img_to_array(img)
    x=np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images)
    ch=''
    if np.argmax(classes)==0:
        ch=' is normal'
    elif np.argmax(classes)==1 :
        ch='is bacteria'
    elif np.argmax(classes)==2:
        ch='is virus'
    else:
        ch='no result'
    return(ch)




#img_normal= mpimg.imread('C:/Users/ramzi/Projet-pfe/Dataset/chest_xray/train/NORMAL/NORMAL2-IM-0535-0001-0002.jpeg')

#ch=predict_label(img_normal)
#print(ch)

# routes
@app.route("/")
def main():
	return render_template("log.html")


@app.route("/", methods = ['GET', 'POST'])
def login():
    user=request.form.get('nombre')
    passw=request.form.get('password')
    if user=="admin" and passw=="adminsarra":
        return render_template("index.html")
    else:
        return render_template("log.html")
        
        
@app.route("/index")
def index_page():
	return render_template("index.html")

@app.route("/submit", methods = ['GET', 'POST'])
def get_output():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "static/" + img.filename	
		img.save(img_path)

		p = predict_label(img_path)
	return render_template("index.html", prediction = p, img_path = img_path)


if __name__ =='__main__':
	#app.debug = True
	app.run(debug = True)
    
