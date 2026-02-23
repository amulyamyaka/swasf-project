from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "YOUR_OPENWEATHER_API_KEY"

# ------------------ WEATHER FUNCTIONS ------------------

def get_weather_by_city(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

# ------------------ FARMING ADVICE ------------------

def generate_advice(temp, condition):
    if condition.lower() == "rain":
        return "Rain expected. Avoid spraying pesticides. Ensure proper drainage."
    elif temp > 35:
        return "High temperature. Irrigate crops early morning or evening."
    elif temp < 15:
        return "Cold weather. Protect crops from frost."
    else:
        return "Weather stable. Good time for regular farming activities."

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    data = request.json

    try:
        if data.get("city"):
            city = data["city"]
            weather_data = get_weather_by_city(city)
        else:
            weather_data = get_weather_by_coords(data["lat"], data["lon"])
            city = weather_data["name"]

        forecast_data = get_forecast(city)

        temp = weather_data["main"]["temp"]
        condition = weather_data["weather"][0]["main"]
        advice = generate_advice(temp, condition)

        forecast_list = []
        for item in forecast_data["list"][:5]:
            forecast_list.append({
                "date": item["dt_txt"],
                "temp": item["main"]["temp"],
                "condition": item["weather"][0]["main"]
            })

        return jsonify({
            "city": city,
            "temperature": temp,
            "condition": condition,
            "advice": advice,
            "forecast": forecast_list
        })

    except:
        return jsonify({"error": "Invalid location or API issue"}), 400


if __name__ == "__main__":
    app.run(debug=True)