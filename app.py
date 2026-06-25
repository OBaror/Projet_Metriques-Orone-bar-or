import requests
from flask import Flask, jsonify, render_template

app = Flask(__name__)


def fetch_json(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


@app.route("/")
def hello_world():
    return render_template("hello.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.get("/paris")
def api_paris():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522&hourly=temperature_2m&forecast_days=7&timezone=Europe%2FParis"
    data = fetch_json(url)
    times = data.get("hourly", {}).get("time", [])
    temps = data.get("hourly", {}).get("temperature_2m", [])
    result = [
        {"datetime": time, "temperature_c": temp}
        for time, temp in zip(times, temps)
    ]
    return jsonify(result)


@app.route("/rapport")
def rapport():
    return render_template("graphique.html")


@app.route("/histogramme")
def histogramme():
    return render_template("histogramme.html")


@app.get("/atelier-data")
def api_atelier():
    url = "https://api.open-meteo.com/v1/forecast?latitude=43.2965&longitude=5.3698&current=wind_speed_10m&hourly=wind_speed_10m&forecast_days=7&timezone=Europe%2FParis"
    data = fetch_json(url)
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    winds = hourly.get("wind_speed_10m", [])
    points = [
        {"datetime": time, "wind_speed": wind}
        for time, wind in zip(times, winds)
    ]
    speeds = [
        wind
        for wind in winds
        if isinstance(wind, int) or isinstance(wind, float)
    ]
    current_speed = data.get("current", {}).get("wind_speed_10m")
    if current_speed is None and speeds:
        current_speed = speeds[0]
    payload = {
        "city": "Marseille",
        "unit": data.get("current_units", {}).get("wind_speed_10m", "km/h"),
        "current": round(float(current_speed or 0), 1),
        "average": round(sum(speeds) / len(speeds), 1) if speeds else 0,
        "maximum": round(max(speeds), 1) if speeds else 0,
        "points": points
    }
    return jsonify(payload)


@app.route("/atelier")
def atelier():
    return render_template("atelier.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
