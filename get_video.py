"""
python3 capture.py /home/susi/Documents/captures/prueba_svo.svo /home/susi/Documents/captures/frames/
"""

import sys
import pyzed.sl as sl
import cv2
import os


def main():
    if len(sys.argv) != 3:
        exit()

    filepath = sys.argv[1]
    outputURL = sys.argv[2]

    print("Reading SVO file: {0}".format(filepath))

    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    cam = sl.Camera()
    status = cam.open(init)

    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    mat = sl.Mat()

    h = 720
    w = 1280

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(outputURL, fourcc, 20.0, (w, h))

    while cv2.waitKey(1) != ord("q"):  # for 'q' key
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(mat)
            im = mat.get_data()
            out.write(im)
            cv2.imshow("frame", im)

    cam.close()
    out.release()
    cv2.destroyAllWindows()

    print("\nFINISH")


if __name__ == "__main__":
    main()
