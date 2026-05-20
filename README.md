# 🚗 Real-Time Driver Drowsiness Detection System using ESP32-CAM

A smart AI-powered **Driver Drowsiness Detection System** using **ESP32-CAM**, **OpenCV**, **MediaPipe**, and a **Flask Web Interface** to monitor driver alertness in real time. The system detects eye closure, yawning, and fatigue symptoms using computer vision techniques and provides instant alerts to prevent road accidents.

---

# 📌 Project Overview

Driver fatigue is one of the leading causes of road accidents worldwide. This project provides a **real-time driver monitoring system** that continuously analyzes facial expressions using an **ESP32-CAM live video stream** and detects drowsiness using **Eye Aspect Ratio (EAR)** and **Mouth Aspect Ratio (MAR)** calculations.

The system is developed using:

* Espressif Systems ESP32-CAM for wireless video streaming
* Flask backend server
* OpenCV for image processing
* MediaPipe for facial landmark detection
* HTML, CSS, JavaScript frontend dashboard
* Real-time audio and visual alert system

---

# ✨ Features

## 🎥 Hardware Features

* ESP32-CAM live video streaming
* Wireless communication over WiFi
* Low-cost embedded solution
* Portable and compact design

## 🧠 AI & Computer Vision

* Real-time face detection
* Eye blink detection using EAR
* Yawning detection using MAR
* Facial landmark tracking with MediaPipe Face Mesh
* Driver fatigue monitoring and classification

## 🌐 Web Dashboard

* Live video stream display
* Real-time driver metrics
* Driver status monitoring
* Alert notifications
* Responsive frontend interface

## 🔔 Alert System

* Audio alarm
* Visual alert warning
* Real-time drowsiness notifications

---

# 🛠️ Technologies Used

| Category  | Technology              |
| --------- | ----------------------- |
| Hardware  | ESP32-CAM, ESP32,       |
|           |Jumping wires, 2 LEDS,   |
|           |USB Cable                |
| Backend   | Python, Flask           |
| Frontend  | HTML5, CSS3, JavaScript3|
| AI/CV     | OpenCV, MediaPipe       |
| Libraries |NumPy,Pandas, seaborn    |

---

# 🏗️ System Architecture

```text
ESP32-CAM → Flask Backend → OpenCV + MediaPipe → Drowsiness Detection → Web Dashboard + Alert System
```

---

# 📂 Project Structure

```bash
Driver-Drowsiness-Detection/
│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── script.js
│   │
│   └── assets/
│       └── alert.wav
│
├── templates/
│   └── index.html
│
├── esp32/
│   └── esp32_cam_code.ino
│
└── model/
    └── detector.py
```

---

# 📦 Requirements

```txt
flask
opencv-python
mediapipe
numpy
imutils
scipy
```

---

# 🚀 Running the Project

## Step 1: Upload ESP32-CAM Code

* Open Arduino IDE
* Select ESP32 Board
* Upload `esp32_cam_code.ino`
* Connect ESP32-CAM to WiFi

---

## Step 2: Run Flask Server

```bash
python app.py
```

---

## Step 3: Open Browser

```text
http://127.0.0.1:5000
```
# 🔧 ESP32-CAM Arduino Code

```cpp
#include "esp_camera.h"
#include <WiFi.h>

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi Connected");
  Serial.println(WiFi.localIP());
}

void loop() {

}
```

---

# 🖥️ Frontend Dashboard

The web dashboard displays:

* Live video stream
* EAR value
* MAR value
* Blink count
* Driver status
* Alert notifications

---

# 📡 API Endpoints

| Endpoint       | Method | Description         |
| -------------- | ------ | ------------------- |
| `/`            | GET    | Dashboard homepage  |
| `/video_feed`  | GET    | Live video stream   |
| `/api/status`  | GET    | Driver status       |
| `/api/metrics` | GET    | EAR and MAR metrics |

---

# 🎯 Applications

* Smart vehicle systems
* Accident prevention systems
* Driver safety monitoring
* Fleet management systems
* Industrial transport monitoring

---

# 📈 Future Enhancements

* Mobile application integration
* Cloud data logging
* GSM emergency alerts
* Night vision support
* AI-based fatigue prediction

---

# ✅ Advantages

✔ Real-time monitoring
✔ AI-based detection
✔ Low-cost implementation
✔ Web-based interface
✔ Easy deployment

---

# ⚠️ Limitations

* Performance may reduce in low light
* Camera angle affects accuracy
* Requires stable WiFi connection

---

# 👨‍💻 Authors

* Bhumika K.R
* Final Year Project 

---

# 📚 References

* Google MediaPipe Documentation
* OpenCV OpenCV Documentation
* Flask Official Documentation
---

# ⭐ Conclusion

The **Real-Time Driver Drowsiness Detection System** is an effective AI-based solution for monitoring driver alertness using computer vision and embedded systems. By integrating ESP32-CAM, Flask, OpenCV, and MediaPipe, the system provides accurate real-time drowsiness detection and enhances road safety.
