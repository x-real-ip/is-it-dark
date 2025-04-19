# 🌓 is-it-dark
A simple API that analyzes an image from a URL and determines how bright it is. Useful for room light detection, camera snapshots, smart home automation, and more.

---

## 🚀 Features

- Accepts an image URL via POST request
- Analyzes brightness using the Python Pillow library
- Returns average brightness value and a brightness **category** (`dark`, `medium`, `bright`)
- Lightweight Flask API, Dockerized for deployment
- Kubernetes-ready

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