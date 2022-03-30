from fastapi import FastAPI
import socket
import requests
import os
import uvicorn

app = FastAPI()


@app.get('/')
def home():
    url = os.environ.get('weather_url')
    if url is None:
        return {"error": "Weather URL is not set on ENV variable"}

    current_state = requests.get(url).json()['current']

    return {
        "hostname": socket.gethostname(),
        "temperature": current_state['temperature'],
        "weather_descriptions": current_state['weather_descriptions'],
        "wind_speed": current_state['wind_speed'],
        "humidity": current_state['humidity'],
        "feelslike": current_state['feelslike']
    }


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=os.environ.get('server_port', 8080))
