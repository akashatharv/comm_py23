import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import pyrealsense2 as rs 
import numpy as np    

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
client_socket.connect((host, 8485))
connection = client_socket.makefile('wb')

#cam = cv2.VideoCapture(0)

#cam.set(3, 320);
#cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    #ret, frame = cam.read()
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_device_from_file("/home/akash/keras-retinanet/rebar_detection_test_17thJune.bag")
    profile = pipe.start(cfg)

    # Skip 5 first frames to give the Auto-Exposure time to adjust
    for x in range(5):
        pipe.wait_for_frames()
  
    # Store next frameset for later processing:
    frameset = pipe.wait_for_frames()
    color_frame = frameset.get_color_frame()
    #depth_frame = frameset.get_depth_frame()

    # Cleanup:
    pipe.stop()
    #print("Frames Captured")
    frame = np.asanyarray(color_frame.get_data())
    #frame = cv2.imread("test_image.png")
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()
