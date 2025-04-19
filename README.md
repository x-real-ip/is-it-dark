# 🌓 is-it-dark
A lightweight API that analyzes images from URLs to determine:

- **Brightness**: Calculates average brightness and categorizes it as `dark`, `medium`, or `bright`.
- **Infrared Detection**: Identifies if the image is likely captured in infrared (grayscale) mode.

Ideal for smart home automation, camera monitoring, and ambient light detection.


---

## 🚀 Features

- Accepts image URLs via POST requests.
- Returns average brightness value and category.
- Detects infrared mode based on color saturation.
- Lightweight Flask API, Dockerized for deployment.
- Kubernetes-ready.

---

## 📦 Requirements

- Python 3.11+
- Docker (optional)

---

## 🛠 Setup

### 🔧 Local Python Setup

```bash
git clone https://github.com/x-real-ip/is-it-dark.git
cd is-it-dark
pip install -r requirements.txt
python app.py
```