# 🌓 is-it-dark
A simple API that analyzes an image from a URL and tells you if it's "dark" or "light". Useful for room light detection, camera snapshots, and IoT automation.

---

## 🚀 Features

- Accepts an image URL via POST request
- Analyzes brightness using PIL (Pillow)
- Returns `{ "is_dark": true/false }`
- Lightweight Flask API, Dockerized

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