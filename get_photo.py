# -*- coding: utf-8 -*- 
import os
from os import listdir
from os.path import isfile, join

def get_photo():
    os.system("sudo modprobe uvcvideo")
    command = "ffmpeg -hide_banner -loglevel panic -f video4linux2 -i /dev/v4l/by-id/usb-CF0D73EA3_Lenovo_EasyCamera_200901010001-video-index0 -vframes 1 /home/nick/Downloads/tg_dump/pic.jpg"
    os.system(command)
    print("A shot was made at") 
    os.system("date")
    print()

