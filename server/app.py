from flask import Flask, request, render_template, jsonify
import util

app = Flask(__name__)
application = app

# Load artifacts at startup - IMPORTANT!
util.load_saved_artifacts()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-locations', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict-home-price', methods=['GET', 'POST'])
def predict_home_price():
    data = request.json
    total_sqft = float(data['total_sqft'])
    location = data['location']
    bhk = int(data['bhk'])
    bath = int(data['bath'])
    response = jsonify({
        'estimated_price': util.get_estimated_price(location,total_sqft,bhk,bath)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    app.run(debug=True)