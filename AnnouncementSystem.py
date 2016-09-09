#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
from urllib.parse import urlparse
from os import curdir, sep
import time
import threading
from socketserver import ThreadingMixIn
import os
import urllib
import sys
import RPi.GPIO as GPIO

SPEAKERS_A = 24
SPEAKERS_B = 25
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKERS_A,GPIO.OUT)
GPIO.setup(SPEAKERS_B,GPIO.OUT)


class Announcement(object):
    type = "file"
    message = ""
    times = 1
    volume = 50
    priority = 100
    id = "general"
    zone = ""

    def __init__(self, type, message, times, volume, priority, id, zone):
        self.type = type
        self.message = message
        self.times = times
        self.volume = volume
        self.priority = priority
        self.id = id
        self.zone = zone

def AnnouncementEquality(a1, a2):
	if(a1.type == a2.type and a1.message == a2.message and a1.times == a2.times and a1.volume == a2.volume and a1.priority == a2.priority and a1.id == a2.id and a1.zone == a2.zone):
		return True
	else:
		return False

def SpeakersOn(zone):
    print("Speakers on in zone ", zone)
    if zone == "A":
        GPIO.output(SPEAKERS_A, True)
    if zone == "B":
        GPIO.output(SPEAKERS_B, True)
    if zone == "C":
        GPIO.output(SPEAKERS_A, True)
        GPIO.output(SPEAKERS_B, True)

def SpeakersOff(zone):
    if zone == "A":
        GPIO.output(SPEAKERS_A, False)
    if zone == "B":
        GPIO.output(SPEAKERS_B, False)
    if zone == "C":
        GPIO.output(SPEAKERS_A, False)
        GPIO.output(SPEAKERS_B, False)


def PlaySound(sound, times, volume, zone):
    print("Playing sound...", sound)
    SpeakersOn(zone)
    #time.sleep(5)
    #set volume
    os.system("amixer sset Speaker " + str(volume) + "%")
    os.system("aplay /var/sounds/" + sound + ".wav")
    SpeakersOff(zone)


AnnQueue=[]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        temp = str(len(AnnQueue))
        o = urlparse(self.path)
        dict = urllib.parse.parse_qs(o.query)
        print("len: ", len(dict))
        if len(dict) == 7:
            t = Announcement(dict['type'][0], dict['message'][0], int(dict['times'][0]), int(dict['volume'][0]), int(dict['priority'][0]), dict['id'][0], dict['zone'][0])
            AnnExists = False
            for ann in AnnQueue:
                if (AnnouncementEquality(ann, t) == True):
                     AnnExists = True
            if AnnExists == False:
                AnnQueue.append(t)
            print("out: ", t.message)
        elif len(dict)== 1:
            for ann in AnnQueue:
                if ann.id == dict['id'][0]:
                    AnnQueue.remove(ann)
        self.wfile.write(bytes(str(temp), "utf-8"))
        print("Client exited")
        return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

server = ThreadedHTTPServer(('',8084), Handler)
t = threading.Thread(target=server.serve_forever)
t.start()


def ProcessQueue():
    AnnQueue.sort(key=lambda x: int(x.priority))
    for ann in AnnQueue:
        if(ann.type == "sound"):
            PlaySound(ann.message, ann.times, ann.volume, ann.zone)
            if(ann.times > 1):
                ann.times = ann.times -1
            elif(ann.times == 1):
                AnnQueue.remove(ann)
                break


while(True):
    ProcessQueue()
    time.sleep(1)


