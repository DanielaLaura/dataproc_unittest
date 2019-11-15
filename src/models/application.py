import pandas as pd
from flask import Flask, jsonify, request
import pickle
 #load model
ta = pickle.load(open('model.pkl','rb'))
# app
application = Flask(__name__)
# routes
@application.route('/data', methods=['POST'])
def prediction():
    # get data and transform to labels
    test= import_clean_data(ind_test, file_test)
    test = import_clean_data(ind_train, file_train)
    y, test_y, y_reg, test_y_reg= get_features_and_labels()

    # predictions
    #ta = TheAlgorithm(y, test_y, y_reg, test_y_reg)
    classification = ta.evaluate_classification()

    # send back to browser
    output = {'results': int(classification[0])}

    # return data
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)