"""
python3 capture.py /home/susi/Documents/captures/prueba_svo.svo
"""

import sys
import pyzed.sl as sl
from signal import signal, SIGINT

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

    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    path_output = sys.argv[1]
    recording_param = sl.RecordingParameters(path_output, sl.SVO_COMPRESSION_MODE.LOSSLESS)
    err = cam.enable_recording(recording_param)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit(1)

    runtime = sl.RuntimeParameters()
    print("SVO is Recording, use Ctrl-C to stop.")
    frames_recorded = 0

    while True:
        if cam.grab(runtime) == sl.ERROR_CODE.SUCCESS:
            frames_recorded += 1
            print("Frame count: " + str(frames_recorded), end="\r")


if __name__ == "__main__":
    main()
