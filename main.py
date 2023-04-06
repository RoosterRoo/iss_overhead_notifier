import time

import requests
from datetime import datetime

MY_LAT = 22.572645
MY_LNG = 88.363892

params = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}


def is_iss_overhead():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()

    data = response.json()
    iss_lat = float(data['iss_position']['latitude'])
    iss_lng = float(data['iss_position']['longitude'])

    if MY_LAT - 5 <= iss_lat <= MY_LAT + 5 and MY_LNG - 5 <= iss_lng <= MY_LNG + 5:
        return True
    return False


def is_it_dark():
    response = requests.get('https://api.sunrise-sunset.org/json', params=params)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T').split(':')[0])
    sunset = int(data['results']['sunset'].split('T').split(':')[0])
    now = datetime.now().hour

    if now >= sunset or now <= sunrise:
        return True
    return False


while True:
    time.sleep(60)
    if is_iss_overhead() and is_it_dark():
        print("Look up👆The ISS satellite is above you...")

