# Human Pose Estimation with Streamlit and Mediapipe

This project demonstrates human pose estimation using Python, OpenCV, and Mediapipe, wrapped in a user-friendly GUI built with Streamlit. Users can detect human poses in images, videos, or through a live webcam feed.

## Features

- **Image Pose Detection**: Upload an image, and the application detects human poses and displays the processed result.
- **Video Pose Detection**:
  - Upload a video, and the application processes it to detect human poses.
  - Live webcam feed processing for real-time pose estimation.
- **Streamlit GUI**: A simple and interactive interface to choose input modes and view results.

# Code Structure

-**process_image(image)**: Processes an uploaded image for pose detection and overlays landmarks.
-**process_video(video_path)**: Processes an uploaded video frame-by-frame for pose detection, saves the output as a new video, and displays it in Streamlit.
-**process_webcam()**: Captures real-time webcam feed, applies pose detection, and displays it within the app.

# Streamlit components:
-**File upload**: Allows users to upload images or videos.
-**Sidebar**: Lets users choose between different input modes.
-**Live feed**: Displays real-time webcam processing.

# Requirements
Python 3.7+
Libraries: streamlit, opencv-python, mediapipe, numpy

# Acknowledgments
Mediapipe for its powerful pose estimation library.
Streamlit for creating interactive web apps with Python.
OpenCV for image and video processing.
