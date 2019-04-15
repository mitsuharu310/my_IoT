# morningSun.py
# Apr14, 15, 2019

from time import sleep
from picamera import PiCamera
from datetime import datetime, timedelta
import requests
import sys


def getCredentials(f_path, name):
    with open(f_path, mode='r') as f:
        for l in f:
            l = l.rstrip()
            if name in l:
                t = l.split('\t')[1]
                c = l.split('\t')[2]
                return t, c


def sendToSlack(file_to_send, ini_comment, token, channel):
    b_file = {'file': open(file_to_send, mode='rb')}
    params = {
              'token': token,
              'channels': channel,
              'filename': 'how_is_this_used',
              'initial_comment': ini_comment,
              'title': file_to_send
              }
    requests.post(url="https://slack.com/api/files.upload",
                  params=params,
                  files=b_file)
    #print(params)
    print(file_to_send, 'sent out!')
    sleep(1)


def myMain():

    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.shutter_speed = 1  # ms
    camera.iso = 10
    sleep(2)

    capture_count = 6
    sleep_sec = 1800
    for i, filename in enumerate(camera.capture_continuous('sun_{counter:02d}-{timestamp:%Y-%m-%d-%H-%M_%S}.jpg')):
        print('Captured:', filename)
        comment = 'capture '
        comment += str(i+1).zfill(2) + ', ' + filename
        sendToSlack(filename, comment, TOKEN, CHANNEL_ID)

        if i == capture_count - 1:
            break
        sleep(sleep_sec)
    print('capture done!')


if __name__ == '__main__':
    TOKEN, CHANNEL_ID = getCredentials(sys.argv[1], sys.argv[2])
    myMain()
