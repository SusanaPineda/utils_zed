"""
python3 capture_loop.py /home/susi/Documents/captures/<nombre_svo_sin_extension>
"""

import sys
import pyzed.sl as sl
from signal import signal, SIGINT
import time

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

    cont = 0

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    while True:
        t = 0
        t0 = time.time()
        path_output = sys.argv[1] + str(cont) + ".svo"
        recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.LOSSLESS)
        err = cam.enable_recording(recording_param)
        if err != sl.ERROR_CODE.SUCCESS:
            print(repr(status))
            exit(1)

        runtime = sl.RuntimeParameters()

        while t < 180:
            if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
                print("grabando \n")
            t = time.time() - t0
            print(str(t))

        cont = cont+1


if __name__ == "__main__":
    main()
