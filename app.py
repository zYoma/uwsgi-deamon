import logging
from flask import Blueprint, Flask, jsonify
from flask import request as flask_request

from config import settings
from utils.ipinfo import GetIpInfo
from utils.openweathermap import GetWeatherInfo


weather = Blueprint('', __name__, url_prefix='/')


def create_app():
    logging.basicConfig(
        filename=settings.LOG_FILE_PATCH,
        level=logging.INFO,
        format='[%(asctime)s] %(levelname).1s %(message)s',
        datefmt='%Y.%m.%d %H:%M:%S',
    )

    app = Flask(__name__)
    app.register_blueprint(weather)

    return app


def get_client_ip(request):
    x_forwarded_for = request.environ.get('HTTP_X_REAL_IP')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.remote_addr
    return ip


@weather.route('/', methods=["GET"])
def get_weather():
    ip = get_client_ip(flask_request)
    coordinates = GetIpInfo(ip)()
    weather_data = GetWeatherInfo(coordinates)()
    result = {
        'city': weather_data.name,
        'temp': weather_data.main.temp,
        'conditions': weather_data.weather[0].description,
    }
    return jsonify(result)


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=6001)
