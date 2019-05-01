# morningSun2.py
# Apr29, 2019

# no capture_continuous loop, one shot version

from time import sleep
from picamera import PiCamera
from datetime import datetime
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
              'filename': file_to_send,
              'initial_comment': ini_comment,
              'title': file_to_send
              }
    requests.post(url="https://slack.com/api/files.upload",
                  params=params,
                  files=b_file)

    print(file_to_send, 'sent out!')


def myMain(TOKEN, CHANNEL_ID, counter):

    filename = 'sun_' + counter.zfill(2) + '_'
    filename += datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.jpg'

    with PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.shutter_speed = 1  # micro sec.
        camera.iso = 10
        camera.start_preview()
        sleep(2)
        camera.capture(filename)

    print('Captured:', filename)
    comment = 'capture ' + counter.zfill(2) + ', ' + filename

    sendToSlack(filename, comment, TOKEN, CHANNEL_ID)

    print('capture done!')


if __name__ == '__main__':
    TOKEN, CHANNEL_ID = getCredentials(sys.argv[1], sys.argv[2])
    counter = sys.argv[3]
    myMain(TOKEN, CHANNEL_ID, counter)
