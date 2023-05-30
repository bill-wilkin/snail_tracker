from flask_app import app
from flask import render_template, redirect, request, session
import math
import os
import requests
from flask import jsonify
count = 0
states = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}
states = dict(map(reversed, states.items()))


@app.route('/')
def index():
    return render_template('index.html', all_states=states.keys())

@app.route('/clear')
def clear():
    session.clear()
    return redirect("/")
@app.route('/calculate', methods=["POST"])
def calculate():
    if 'count' not in session:
        session['count']= 0
    session['count']+=1
    you_city = request.form['you_city'].replace(" ", "%20")
    snail_city = request.form['snail_city'].replace(" ", "%20")
    you_state = states[request.form['you_state']]
    snail_state = states[request.form['snail_state']]

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?destinations={you_city}%2{you_state}&origins={snail_city}%2{snail_state}&units=imperial&key={os.environ['DISTANCE_KEY']}"
    print(f"URL: {url}")

    payload={}
    headers = {}

    r = requests.request("GET", url)
    response = r.json()
    
    print(response)
    print(response['rows'][0]['elements'][0]['distance']['text'][:-3])
    


    miles = float(response['rows'][0]['elements'][0]['distance']['text'][:-3].replace(',',''))
    snail_speed = 0.03
    hours = round(miles/snail_speed, 2)
    days = round(hours/24, 2)
    days_remainder = round(days-math.floor(days), 2)
    hours = round(days_remainder*24, 2)
    hours_remainder = round(hours-math.floor(hours), 2)
    minutes = round(hours_remainder*60, 2)
    minutes_remainder = round(minutes-math.floor(minutes), 2)
    seconds = round(minutes_remainder*60, 2)
    seconds_remainder = round(seconds-math.floor(seconds), 2)

    session['days'] = math.floor(days)
    session['hours'] = math.floor(hours)
    session['minutes'] = math.floor(minutes)
    session['seconds'] = math.floor(seconds)

    return redirect('/')
