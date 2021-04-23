
import cv2
import numpy as np
import pyzed.sl as sl
import time
import datetime

camera_settings = sl.VIDEO_SETTINGS.BRIGHTNESS
str_camera_settings = "BRIGHTNESS"
step_camera_settings = 1


def main():
    print("Running...")
    init = sl.InitParameters()
    init.camera_resolution = sl.RESOLUTION.HD720
    init.camera_fps = 30
    init.depth_mode = sl.DEPTH_MODE.ULTRA  # Use ULTRA depth mode
    init.coordinate_units = sl.UNIT.METER
    init.depth_minimum_distance = 0.15

    cam = sl.Camera()
    if not cam.is_opened():
        print("Opening ZED Camera...")
    status = cam.open(init)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    mat = sl.Mat()
    m = np.zeros((120, 120))

    t0 = time.time()
    while cv2.waitKey(1) != ord("q"):  # for 'q' key
        cv2.imshow("m", m)
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            name = datetime.datetime.now()
            path_output = name.strftime("%d_%m_%Y__%H_%M_") + ".png"
            if ((time.time() - t0) > 1800) or (cv2.waitKey(1) == ord("c")):
                cam.retrieve_image(mat, sl.VIEW.LEFT)
                cv2.imshow("ZED", mat.get_data())
                cv2.imwrite(path_output, mat.get_data())
                t0 = time.time()
                print("imagen nueva")
    cv2.destroyAllWindows()

    cam.close()
    print("\nFINISH")



if __name__ == "__main__":
    main()