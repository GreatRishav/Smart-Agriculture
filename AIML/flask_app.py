from flask import Flask, request, jsonify, render_template
import pickle
import requests
import os

app = Flask(__name__)

MODEL_PATH = "/home/tmslece/mysite/knn_model.pkl"
THINGSPEAK_URL = 'https://api.thingspeak.com/channels/2535721/feeds.json'
API_KEY = 'NCG9CGQ8RJNV35HF'


def load_model():
    """Loads and returns the model from a pickle file."""
    try:
        with open(MODEL_PATH, 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        return None


def predict_placement(mst, tem):
    """Predicts placement based on moisture and temperature."""
    model = load_model()
    if model is None:
        return None
    return model.predict([[mst, tem]])[0]


@app.route('/predict', methods=['POST'])
def predict():
    mst = float(request.form.get('moisture'))
    tem = float(request.form.get('temperature'))
    result = predict_placement(mst, tem)

    if result is None:
        return jsonify({'error': 'Model not found'}), 500

    return jsonify({'placement': str(result)})


@app.route('/createcm')
def createcm():
    mst = request.args.get('moisture')
    tem = request.args.get('temperature')

    if mst is None or tem is None:
        return jsonify({'error': 'Missing moisture or temperature parameter'}), 400

    result = predict_placement(float(mst), float(tem))

    if result is None:
        return jsonify({'error': 'Model not found'}), 500

    return jsonify({'placement': str(result)})


@app.route("/")  # render the website
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])  # submit the form
def make_prediction():
    if request.method == 'POST':
        mst = float(request.form['moisture'])
        tem = float(request.form['temperature'])
        result = predict_placement(mst, tem)

        if result is None:
            return render_template('error.html', error_message='Model not found')

        return render_template('prediction.html', result=result)

    return render_template('index.html')


@app.route('/fetch_thingspeak', methods=['GET'])
def fetch_thingspeak():
    try:
        response = requests.get(f"{THINGSPEAK_URL}?api_key={API_KEY}&results=1")
        response.raise_for_status()
        data = response.json()

        # Extract the latest data point
        mst = data['feeds'][0].get('field1')  # Adjust field index based on your ThingSpeak setup
        tem = data['feeds'][0].get('field2')

        if mst is None or tem is None:
            return jsonify({'error': 'Incomplete data received from ThingSpeak'}), 400

        return jsonify({'moisture': mst, 'temperature': tem})

    except requests.RequestException as e:
        return jsonify({'error': f'Error fetching data from ThingSpeak: {e}'}), 500


@app.route('/predict_from_thingspeak', methods=['GET'])
def predict_from_thingspeak():
    fetch_response = fetch_thingspeak()

    if fetch_response.status_code != 200:
        return fetch_response

    fetch_data = fetch_response.get_json()
    mst = float(fetch_data['moisture'])
    tem = float(fetch_data['temperature'])

    result = predict_placement(mst, tem)

    if result is None:
        return jsonify({'error': 'Model not found'}), 500

    return jsonify({'placement': str(result)})


if __name__ == '__main__':
    app.run(debug=True)
