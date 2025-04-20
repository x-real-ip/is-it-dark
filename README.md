# 🌓 is-it-dark

- [🌓 is-it-dark](#-is-it-dark)
  - [🚀 Features](#-features)
  - [📦 Requirements](#-requirements)
  - [🛠 Setup](#-setup)
    - [Local Python Setup](#local-python-setup)
    - [Podman or Docker](#podman-or-docker)
  - [⚙️ Configuration via `config.yaml`](#️-configuration-via-configyaml)
    - [Example `config.yaml`:](#example-configyaml)
    - [Kubernetes](#kubernetes)

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

You can run the image-light-detector API in multiple ways:

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
docker run -p 5000:5000 your-dockerhub-username/image-light-detector:latest
```

If you want to customize the config:

```bash
docker run -p 5000:5000 -v $(pwd)/config.yaml:/app/config.yaml:ro your-dockerhub-username/image-light-detector:latest
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

### Kubernetes

This service is **Kubernetes-ready** a manifest yaml example can be found
[here](https://github.com/x-real-ip/gitops/tree/main/manifests/is-it-dark)
