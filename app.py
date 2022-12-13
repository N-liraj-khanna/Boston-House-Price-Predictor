from flask import Flask,request,jsonify,url_for,render_template
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

import warnings
warnings.filterwarnings('ignore')

# Initialize the flask server, this is where the site starts
app=Flask(__name__)

# Load the model and scaler
model=pickle.load(open("ML Model/regression-model.pkl", 'rb')) 
sc=pickle.load(open("ML Model/scaling.pkl", 'rb'))

# The home route init
@app.route('/')
def home():
  return render_template("home.html")

@app.route('/predict_api', methods=['POST'])
def predict_api():
  data=request.json['data']
  print(data)
  conv_data=np.array(list(data.values())).reshape(1,-1)
  new_data=sc.transform(conv_data)
  output=model.predict(new_data)
  print(output[0])
  return jsonify(output[0])

@app.route('/predict',methods=[ 'POST'])
def predict():
  data=[float(x) for x in request.form.values()]
  print(data)
  final_input=sc.transform(np.array(data).reshape(1,-1))
  print(final_input)
  output=model.predict(final_input) [0]
  return render_template("home.html", prediction_text="The predicted house price is {}".format(output))

if __name__ == "__main__":
  app.run(debug=True)