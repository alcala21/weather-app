from flask import Flask, render_template, request
import requests
import sys
from weather.api import key

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        city = request.form['city_name']
        if city:
            info = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={key}")
            if info.status_code == 200:
                data = info.json()
                temperature = data['main']['temp']
                state = data['weather'][0]['main']#
                dict_with_weather_info = {"city": city, "temperature": temperature, "state": state}
                return render_template("index.html", weather=dict_with_weather_info)
    return render_template("index.html", weather=None)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
