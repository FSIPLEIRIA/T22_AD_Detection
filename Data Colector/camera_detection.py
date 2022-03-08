import glob
import math
import os
import sys
import time

import PIL
import pyrealsense2 as rs
import numpy as np
import cv2
from classes.Pixel import Pixel

# Field of views values for D435 camera

HORIZONTAL_FOV = 86
VERTICAL_FOV = 57
DIAGONAL_FOV = 94

CAMERA_RESOLUTION_WIDTH = 848
CAMERA_RESOLUTION_HEIGHT = 480

FRAMES_FOLDER = "frames"

np.set_printoptions(threshold=sys.maxsize)  # to print the whole matrix

def empty_directory(directory_name):
    for file in os.listdir(directory_name):
        os.remove(os.path.join(directory_name, file))

def get_camera_feed_frames():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    found_rgb = False
    for s in device.sensors:
        if s.get_info(rs.camera_info.name) == 'RGB Camera':
            found_rgb = True
            break
    if not found_rgb:
        print("The demo requires Depth camera with Color sensor")
        exit(0)

    config.enable_stream(rs.stream.depth, CAMERA_RESOLUTION_WIDTH, CAMERA_RESOLUTION_HEIGHT, rs.format.z16, 30)

    if device_product_line == 'L500':
        config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
    else:
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start streaming
    pipeline.start(config)

    try:
        #empty frame folder
        empty_directory(FRAMES_FOLDER)

        count = 0
        while True:
            time.sleep(1)
            print("frame %d" % count)
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            depth_colormap_dim = depth_colormap.shape
            color_colormap_dim = color_image.shape

            # If depth and color resolutions are different, resize color image to match depth image for display
            if depth_colormap_dim != color_colormap_dim:
                resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]),
                interpolation=cv2.INTER_AREA)
                images = np.hstack((resized_color_image, depth_colormap))
            else:
                images = np.hstack((color_image, depth_colormap))

            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            cv2.waitKey(1)

            #save frame to jpg file
            filename = "frames/frame_%d.jpg" % count
            cv2.imwrite(filename, images)
            count+=1

            #calculate frame file pixel values
            get_frame_pixel_distance(filename, depth_frame, color_frame)

    finally:

        # Stop streaming
        pipeline.stop()

#get x and y values for each pixel and the depth value
def read_image_data(filename):
    image = PIL.Image.open(filename)
    width, height = image.size

    print(width, height)

    # empty matrix for pixel values (x, y, depth and cone_color) foreach frame
    camera_feed_pixel_indexes_matrix = np.zeros((width, height))

#Calculate the distance to a pixel in a frame
def get_frame_pixel_distance(filename, depth_frame, color_frame):

    read_image_data(filename)

    x = 0
    y = 0

    depth = depth_frame.get_distance(x, y)
    color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
    dx, dy, dz = rs.rs2_deproject_pixel_to_point(color_intrin, [x, y], depth)
    distance = math.sqrt(((dx) ** 2) + ((dy) ** 2) + ((dz) ** 2))
    print("Distance from camera to pixel:", distance)
    print("Z-depth from camera surface to pixel surface:", depth)

get_camera_feed_frames()