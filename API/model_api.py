from flask import Flask, request, jsonify
from sklearn.externals import joblib
import traceback
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if model:
        try:
            json_ = request.json
            print(json_)
            query = pd.DataFrame(json_, index=[0], columns=model_columns)
            
            prediction = list(model.predict(query))
            return jsonify({'prediction': prediction})
        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Load the model')
        return 'Model is undefined'


if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
    except:
        port = 12345

    model = joblib.load('model.pkl')
    print('Model loaded')
    model_columns = joblib.load('model_columns.pkl')
    print('Model columns loaded')

    app.run(port = port, debug=True)
