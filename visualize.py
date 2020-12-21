"""
python3 capture.py /home/susi/Documents/captures/prueba_svo.svo
"""

import sys
import pyzed.sl as sl
import cv2


def main():
    if len(sys.argv) != 2:
        exit()

    filepath = sys.argv[1]
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

    while cv2.waitKey(1) != ord("q"):  # for 'q' key
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            #cam.retrieve_image(mat)
            cam.retrieve_measure(mat, sl.MEASURE.DEPTH, sl.MEM.CPU)
            cv2.imshow("ZED", mat.get_data())

    cv2.destroyAllWindows()
    cam.close()
    print("\nFINISH")


if __name__ == "__main__":
    main()
