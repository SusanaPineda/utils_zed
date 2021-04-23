"""
python3 capture.py /home/susi/Documents/captures/prueba_svo.svo /home/susi/Documents/captures/frames/ /home/susi/Documents/captures/depth/
"""

import sys
import pyzed.sl as sl
import cv2
import os


def main():
    if len(sys.argv) != 4:
        exit()

    filepath = sys.argv[1]
    rgb = sys.argv[2]
    depth = sys.argv[3]
    print("Reading SVO file: {0}".format(filepath))

    input_type = sl.InputType()
    input_type.set_from_svo_file(filepath)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.depth_mode = sl.DEPTH_MODE.ULTRA
    cam = sl.Camera()
    status = cam.open(init)

    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    runtime = sl.RuntimeParameters()
    runtime.sensing_mode = sl.SENSING_MODE.FILL

    mat_img = sl.Mat()
    mat_depth = sl.Mat()
    fr = 0
    cont = 0
    while cv2.waitKey(1) != ord("q"):  # for 'q' key
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            if cont == 2:
                cam.retrieve_image(mat_img)
                cam.retrieve_image(mat_depth, sl.VIEW.DEPTH)
                im = mat_img.get_data()
                d = mat_depth.get_data()
                cv2.imshow("ZED", mat_img.get_data())
                cv2.imwrite(os.path.join(rgb, filepath.split('/')[-1].split('.')[0] + '-' + str(fr))+".png", im)
                cv2.imwrite(os.path.join(depth, filepath.split('/')[-1].split('.')[0] + '-' + str(fr))+".png", d)
                fr = fr + 1
                cont = 0
            else:
                cont = cont + 1

    cv2.destroyAllWindows()
    cam.close()
    print("\nFINISH")


if __name__ == "__main__":
    main()
