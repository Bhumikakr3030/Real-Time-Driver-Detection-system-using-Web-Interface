from flask import Flask, render_template, Response, jsonify
import cv2
import mediapipe as mp
import time
import math
import threading
import serial
import time

class BuzzerController:
    def __init__(self, port='COM3', baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for ESP32 to reset

    def buzzer(self, condition):
        """
        condition = True  -> Turn ON
        condition = False -> Turn OFF
        """
        if condition:
            self.ser.write(b'1')
            print("Buzzer ON")
        else:
            self.ser.write(b'2')
            print("Buzzer OFF")

    def close(self):
        self.ser.close()


app = Flask(__name__)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True, max_num_faces=1)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Shared state (thread-safe)
state = {
    "status": "AWAKE",
    "ear": 0.25,
    "mar": 0.0,           # we'll add simple mouth later or keep 0.45
    "perclos": 15,
    "blink_rate": 0.3,
    "drowsy_events": 0,
    "alert_level": 1,
    "detection_time": "00:00",
    "logs": ["System initialized. Ready to start detection."],
    "face_detected": False,
    "detection_active": False
}
lock = threading.Lock()
start_time = None

def euclidean(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def ear(landmarks, eye):
    v1 = euclidean(landmarks[eye[1]], landmarks[eye[5]])
    v2 = euclidean(landmarks[eye[2]], landmarks[eye[4]])
    h = euclidean(landmarks[eye[0]], landmarks[eye[3]])
    return (v1 + v2) / (2.0 * h) if h > 1e-6 else 0.0

def generate_frames():
    cap = cv2.VideoCapture("http://192.168.134.54:81/")
    #cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', cv2.imread('error.jpg'))[1].tobytes() + b'\r\n'
        return

    frame_count = 0
    closed_frames = 0
    last_blink = time.time()

    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = face_mesh.process(rgb)

        with lock:
            state["face_detected"] = bool(res.multi_face_landmarks)
            if state["detection_active"]:
                frame_count += 1

        color = (0, 255, 0)
        text = "AWAKE"

        if res.multi_face_landmarks:
            lm = res.multi_face_landmarks[0].landmark
            left = ear(lm, LEFT_EYE)
            right = ear(lm, RIGHT_EYE)
            curr_ear = (left + right) / 2

            with lock:
                state["ear"] = round(curr_ear, 2)

            # Very simple blink & PERCLOS approximation
            if curr_ear < 0.24:
                closed_frames += 1
                if time.time() - last_blink > 3 and curr_ear < 0.18:
                    last_blink = time.time()
                    with lock:
                        state["blink_rate"] = round(state["blink_rate"] + 0.1, 1)
            perclos = round((closed_frames / max(1, frame_count)) * 100, 0) if frame_count > 0 else 15

            with lock:
                state["perclos"] = int(perclos)

            if curr_ear < 0.24:
                text = "EYES CLOSED"
                color = (0, 165, 255)
                if (time.time() - state.get("closed_start", 0)) > 2:
                    text = "DROWSY ALERT!"
                    color = (0, 0, 255)
                    buzzer = BuzzerController('COM5')

                    buzzer.buzzer(True)   # ON
                    time.sleep(3)

                    buzzer.buzzer(False)  # OFF

                    buzzer.close()

                    with lock:
                        if state["status"] != "DROWSY ALERT!":
                            state["drowsy_events"] += 1
                            state["alert_level"] = min(state["alert_level"] + 1, 5)
                            state["logs"].insert(0, f"{time.strftime('%H:%M:%S')} Drowsiness detected!")
        else:
            text = "NO FACE"

        cv2.putText(frame, f"Status: {text}", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

        with lock:
            state["status"] = text
            if state["detection_active"]:
                elapsed = time.time() - start_time
                mins, secs = divmod(int(elapsed), 60)
                state["detection_time"] = f"{mins:02d}:{secs:02d}"

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()

@app.route('/')
def home():
    return render_template('home.html')   

@app.route('/monitor')
def monitor():
    return render_template('monitor.html')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/state')
def get_state():
    with lock:
        return jsonify(state)

@app.route('/api/start', methods=['POST'])
def start():
    global start_time
    with lock:
        if not state["detection_active"]:
            state["detection_active"] = True
            start_time = time.time()
            state["logs"].insert(0, f"{time.strftime('%H:%M:%S')} Detection started")
    return '', 204

@app.route('/api/stop', methods=['POST'])
def stop():
    with lock:
        state["detection_active"] = False
        state["logs"].insert(0, f"{time.strftime('%H:%M:%S')} Detection stopped")
    return '', 204

@app.route('/api/reset', methods=['POST'])
def reset():
    with lock:
        state.update({
            "status": "AWAKE", "ear":0.25, "perclos":15, "blink_rate":0.3,
            "drowsy_events":0, "alert_level":1, "detection_time":"00:00",
            "logs": ["System reset"], "detection_active":False
        })
    return '', 204

if __name__ == '__main__':
    app.run(debug=True, threaded=True)