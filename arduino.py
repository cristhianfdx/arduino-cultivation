import time

import requests
import serial
from requests.exceptions import HTTPError


def read_arduino_data():
    print('Running. Press CTRL-C to exit.')
    with serial.Serial("COM7", 9600, timeout=1) as arduino:
        time.sleep(0.1)
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    while arduino.inWaiting() == 0:
                        pass
                    if arduino.inWaiting() > 0:
                        answer = arduino.readline()
                        data = str(answer).replace('b', '').replace('\'', '')
                        send_data_to_server(get_request(data.split(',')))
                        arduino.flushInput()
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")


def get_request(values):
    request = []

    sensor = None
    for val in values:
        sensor = val.split(':')
        request.append({
            'type': sensor[0],
            'value': sensor[1]
        })

    print(request)
    return request


def send_data_to_server(req):
    url = 'http://127.0.0.1:3000/api/sensors'
    try:
        response = requests.post(url, json=req)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')


if __name__ == '__main__':
    read_arduino_data()
