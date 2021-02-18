"""
python3 capture.py /home/susi/Documents/captures/
"""

import sys
import pyzed.sl as sl
from signal import signal, SIGINT
import gpsd
import time
import datetime

cam = sl.Camera()
cam.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, 0)


def handler(signal_received, frame):
    cam.disable_recording()
    cam.close()
    sys.exit(0)


signal(SIGINT, handler)


def main():
    if not sys.argv or len(sys.argv) != 2:
        exit(1)

    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_fps = 30
    init.depth_mode = sl.DEPTH_MODE.ULTRA  # Use ULTRA depth mode
    init.coordinate_units = sl.UNIT.METER
    init.depth_minimum_distance = 0.15


    gpsd.connect()
    packet = gpsd.get_current()

    print("  Mode: " + str(packet.mode))

    cont = 0

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    ########
    while True:
        t = 0
        t0 = time.time()
        name = datetime.datetime.now()
        path_output = name.strftime("%d_%m_%Y__%H_%M_") + ".svo"
        path_output = sys.argv[1] + str(cont) + path_output
        recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.LOSSLESS)
        err = cam.enable_recording(recording_param)
        if err != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            exit(1)

        file = open(path_output.split('.')[0] + ".txt", 'w')

        runtime = sl.RuntimeParameters()

        while t < 60:
            if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
                file.write(str(packet.lat) + " " + str(packet.lon) + " " + str(packet.track) + "\n")
                print(str(packet.lat) + " " + str(packet.lon) + " " + str(packet.track) + "\n")
            t = time.time() - t0
            print(str(t))

        file.close()
        cont = cont+1
        ###

if __name__ == "__main__":
    main()
