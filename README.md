# 🌓 is-it-dark

- [🌓 is-it-dark](#-is-it-dark)
  - [🚀 Features](#-features)
  - [📦 Requirements](#-requirements)
  - [🛠 Setup](#-setup)
    - [Local Python Setup](#local-python-setup)
    - [Podman or Docker](#podman-or-docker)
    - [Kubernetes](#kubernetes)
  - [⚙️ Configuration via `config.yaml`](#️-configuration-via-configyaml)
    - [Example `config.yaml`:](#example-configyaml)
  - [🖥️ API Usage](#️-api-usage)
    - [Image Analysis Request (POST)](#image-analysis-request-post)
      - [Example Request](#example-request)
      - [Example API Response](#example-api-response)

A lightweight API that analyzes images from URLs to determine:

- **Brightness**: Calculates average brightness and categorizes it as `dark`,
  `medium`, or `bright`.
- **Infrared Detection**: Identifies if the image is likely captured in infrared
  (grayscale) mode.

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

You can run the is-it-dark API in multiple ways:

---

### Local Python Setup

```bash
git clone https://github.com/x-real-ip/is-it-dark.git
cd is-it-dark
pip install -r requirements.txt
python app.py
```

### Podman or Docker

```bash
docker run -p 5000:5000 ghcr.io/x-real-ip/is-it-dark:latest
```

If you want to customize the config:

```bash
docker run -p 5000:5000 -v $(pwd)/config.yaml:/app/config.yaml:ro ghcr.io/x-real-ip/is-it-dark:latest
```

Podman or Docker compose:

```yaml
version: "3.8"

services:
  is-it-dark:
    image: ghcr.io/x-real-ip/is-it-dark:latest
    container_name: is-it-dark
    ports:
      - "5000:5000"
    volumes:
      - ./config.yaml:/app/config.yaml:ro # Optional: mount config file
    restart: unless-stopped
```

```bash
docker-compose up -d
```

### Kubernetes

This service is **Kubernetes-ready** a manifest yaml example can be found
[here](https://github.com/x-real-ip/gitops/tree/main/manifests/is-it-dark)

## ⚙️ Configuration via `config.yaml`

You can manage brightness thresholds and infrared detection settings without
editing code.

> **The config file must be located at:**  
> `/app/config.yaml` inside the container (or relative to `app.py` when running
> locally).

### Example `config.yaml`:

```yaml
brightness_thresholds:
  dark: 85
  medium: 170
  # Anything above 170 will be marked as "bright"

infrared_threshold: 10
# If the average saturation is below this threshold, the image will be considered infrared.
```

## 🖥️ API Usage

Once the service is running, you can call the API to check if an image is dark
or light, and to detect if it's infrared or color. In other words, it gives
parameters to answer to the question, is it dark?

### Image Analysis Request (POST)

Send a `POST` request with an image to get the **dark/light** and
**infrared/color** result.

#### Example Request

```bash
curl -X POST "http://localhost:5000/analyze" \
     -F "image=@path/to/your/image.jpg"
```

- Replace localhost:5000 with your server URL if running remotely.
- The image=@path/to/your/image.jpg part sends the image for analysis.

Example Request (Using Python's requests library):

```python
import requests

url = "http://localhost:5000/analyze"
files = {'image': open('path/to/your/image.jpg', 'rb')}
response = requests.post(url, files=files)

print(response.json())  # Returns the analysis result in JSON
```

#### Example API Response

The response will be in JSON format with two fields: is_dark and infrared:

```json
{
  "brightness": 75.4,
  "is_dark": true,
  "infrared": false
}
```

- is_dark: true if the image is considered "dark" based on the brightness
  threshold.
- infrared: true if the image is detected as infrared (based on the infrared
  threshold).
- brightness: The calculated brightness of the image (a float value,
  representing the overall brightness level of the image).
