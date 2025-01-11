import streamlit as st
import cv2
import mediapipe as mp
import tempfile
import os
import numpy as np


mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def process_image(image):
    """Process and display pose estimation for an image."""
    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    return image

def process_video(video_path):
    """Process and display pose estimation for a video."""
    cap = cv2.VideoCapture(video_path)
    output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    with mp_pose.Pose() as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            out.write(frame)
    cap.release()
    out.release()
    return output_path

def process_webcam():
    """Process webcam feed in real-time."""
    cap = cv2.VideoCapture(0)
    
    stop_button = st.button("Stop Webcam")
    
    with mp_pose.Pose() as pose:
        stframe = st.empty()
        while cap.isOpened() and not stop_button:
            ret, frame = cap.read()
            if not ret:
                break
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            stframe.image(frame, channels="BGR")
            
            if stop_button:
                break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    st.title("Human Pose Estimation")
    st.sidebar.title("Choose Input Type")
    mode = st.sidebar.radio("Select Mode", ["Image", "Video"])

    if mode == "Image":
        uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
        if uploaded_image:
            file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            processed_image = process_image(image)
            st.image(processed_image, channels="BGR", caption="Processed Image")

    elif mode == "Video":
        video_mode = st.sidebar.radio("Video Input", ["Upload Video", "Live Webcam"])
        if video_mode == "Upload Video":
            uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "avi", "mov"])
            if uploaded_video:
                temp_file = tempfile.NamedTemporaryFile(delete=False)
                temp_file.write(uploaded_video.read())
                output_video_path = process_video(temp_file.name)
                st.video(output_video_path)
                os.remove(temp_file.name)
                os.remove(output_video_path)
        elif video_mode == "Live Webcam":
            st.warning("Press 'Stop' in Streamlit to exit webcam.")
            process_webcam()
