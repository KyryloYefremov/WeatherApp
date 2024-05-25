#!/usr/bin/env bash

virtualenv /home/ubuntu/env
source /home/ubuntu/env/bin/activate
pip install gunicorn
pip install -r /home/ubuntu/WeatherApp/requirements.txt