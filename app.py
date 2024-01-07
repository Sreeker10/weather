from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Replace 'your_api_key' with your actual WeatherAPI key
API_KEY = '36330ab1222f487fb2260325240701'

def get_weather(city, country):
    base_url = "https://api.weatherapi.com/v1/current.json"
    params = {
        'q': f"{city},{country}",
        'key': API_KEY,
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data.get('current', {}).get('temp_c')
            description = data.get('current', {}).get('condition', {}).get('text')
            if temperature is not None and description is not None:
                return {'temperature': temperature, 'description': description}
            else:
                return {'error': 'Temperature or description not found in the API response'}
        else:
            return {'error': data.get('error', {}).get('message', 'Unknown error')}
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_weather', methods=['GET'])
def api_get_weather():
    city = request.args.get('city')
    country = request.args.get('country')

    # Ensure both city and country are provided before calling get_weather
    if city and country:
        weather_data = get_weather(city, country)
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Both city and country are required'})

if __name__ == '__main__':
    app.run(debug=True)
