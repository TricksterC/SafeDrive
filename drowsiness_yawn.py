from flask import Flask, render_template
from flask_socketio import SocketIO
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2
import serial
import os
import threading

app = Flask(__name__)  # Fix: Use __name__ instead of _name_
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize serial communication with Arduino (with timeout and delay)
try:
    arduino = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2)  # Allow time for Arduino to initialize
except serial.SerialException as e:
    print(f"Error connecting to Arduino: {e}")
    arduino = None  # Prevent crash if Arduino is unavailable

# Constants
EYE_AR_THRESH = 0.30
EYE_AR_CONSEC_FRAMES = 25
YAWN_THRESH = 18
eye_counter = 0
last_status = "NONE"

# Load face detection models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat'))

vs = VideoStream(src=0).start()
time.sleep(1.0)  # Allow camera to warm up

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def final_ear(shape):
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    return (leftEAR + rightEAR) / 2.0

def lip_distance(shape):
    top_lip = np.concatenate((shape[50:53], shape[61:64]))
    low_lip = np.concatenate((shape[56:59], shape[65:68]))
    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)
    return abs(top_mean[1] - low_mean[1])

@app.route('/')
def index():
    return render_template('index.html')

def process_frame():
    global eye_counter, last_status
    while True:
        frame = vs.read()
        if frame is None:
            break
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use Dlib's detector instead of OpenCV
        rects = detector(gray)
        print(f"Number of faces detected: {len(rects)}")  # Debug: Check face detection

        shut_eye_alert = False
        yawn_alert = False
        ear = 0.0
        distance = 0.0

        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            print(f"Landmarks detected: {len(shape)}")  # Debug: Check landmark detection

            ear = final_ear(shape)
            distance = lip_distance(shape)
            print(f"EAR: {ear}, Yawn: {distance}")  # Debug: Print EAR and Yawn values

            if ear < EYE_AR_THRESH:
                eye_counter += 1
                if eye_counter >= EYE_AR_CONSEC_FRAMES:
                    shut_eye_alert = True
            else:
                eye_counter = 0

            if distance > YAWN_THRESH:
                yawn_alert = True

            # Visualize landmarks for debugging
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

        # Determine new status
        new_status = "NONE"
        if shut_eye_alert:
            new_status = "SHUT_EYE"
        elif yawn_alert:
            new_status = "YAWN"

        # Send data only if status changes
        if new_status != last_status:
            print(f"Sending to Arduino: {new_status}")
            if arduino:
                arduino.write(f"{new_status}\n".encode())  # Convert string to bytes
            print(f"Emitting WebSocket event: drowsiness_alert, status: {new_status}")  # Debug log
            socketio.emit('drowsiness_alert', {'status': new_status})
            last_status = new_status

        # Display EAR and Yawn Distance on the frame
        cv2.putText(frame, f"EAR: {ear:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Yawn: {distance:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Display frame with detection
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC key to exit
            break

    cv2.destroyAllWindows()
    vs.stop()
    if arduino:
        arduino.close()

if __name__ == '__main__':
    # Start the frame processing in a separate thread
    frame_thread = threading.Thread(target=process_frame)
    frame_thread.daemon = True
    frame_thread.start()

    # Run the Flask-SocketIO app
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)