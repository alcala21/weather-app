from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
import requests
import sys
from weather.api import key, wurl
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SECRET_KEY'] = 'mi-clave-secreta'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<City {self.name}>"


db.create_all()


@app.route("/")
def index():
    return render_template("index.html", cities=City.query.all())


@app.route("/add", methods=['POST'])
def add_city_weather():
    city_name = request.form.get('city_name')

    if not city_name:
        flash("The city doesn't exist!")
        return redirect('/')

    if City.query.filter_by(name=city_name).first():
        flash("The city has already been added to the list!")
        return redirect('/')

    wparams = {'q': city_name, 'appid': key, 'units': 'metric'}
    info = requests.get(wurl, params=wparams)
    if info.status_code == 200:
        data = info.json()
        loc_city = City(
                        name=city_name,
                        temperature=int(data['main']['temp']),
                        state=data['weather'][0]['main']
                        )
        db.session.add(loc_city)
        db.session.commit()
    else:
        flash("The city doesn't exist!")

    return redirect("/")


@app.route('/delete/<city_id>', methods=['POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
