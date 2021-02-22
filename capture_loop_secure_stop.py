"""
python3 capture_loop.py
"""

import sys
import pyzed.sl as sl
from signal import signal, SIGINT
import time
import RPi.GPIO as GPIO
import subprocess
import shlex
import datetime

cam = sl.Camera()
cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, 0)

input_pin = 18


def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)


signal(SIGINT, handler)


def main():
    if not sys.argv or len(sys.argv) != 1:
        exit(1)

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_fps = 30
    init.depth_mode = sl.DEPTH_MODE.ULTRA  # Use ULTRA depth mode
    init.coordinate_units = sl.UNIT.METER
    init.depth_minimum_distance = 0.15

    cont = 0
    if not cam.is_opened():
    	print("Opening ZED Camera...")
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status)+'Camara no inicializada')
        #exit(1)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(input_pin, GPIO.IN)
    
    value = GPIO.input(input_pin)

    while value:
        t = 0
        t0 = time.time()
        name = datetime.datetime.now()
        path_output = name.strftime("%d_%m_%Y__%H_%M_") + ".svo"
        recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.LOSSLESS)
        err = cam.enable_recording(recording_param)
        if err != sl.ERROR_CODE.SUCCESS:
            print(repr(status)+'Error al crear el archivo')
            #exit(1)

        runtime = sl.RuntimeParameters()

        while (t < 180) and (value):
            if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
                print("grabando \n")
            t = time.time() - t0
            #print(str(t))
            value = GPIO.input(input_pin)
            print(value)

        cont = cont+1
        
    if not value:
    	cmd = shlex.split("shutdown -h now")
    	subprocess.call(cmd)


if __name__ == "__main__":
    main()
