from flask import Flask, request, jsonify
from PIL import Image
import colorsys
import requests
import io
import yaml

with open("config.yaml") as f:
    CONFIG = yaml.safe_load(f)


app = Flask(__name__)


def analyze_image_brightness(image):
    grayscale = image.convert("L")
    histogram = grayscale.histogram()
    pixels = sum(histogram)

    if pixels == 0:
        raise ValueError("Empty image")

    brightness = sum(i * histo for i, histo in enumerate(histogram)) / pixels

    dark_thresh = CONFIG["brightness_thresholds"]["dark"]
    medium_thresh = CONFIG["brightness_thresholds"]["medium"]

    if brightness < dark_thresh:
        category = "dark"
    elif brightness < medium_thresh:
        category = "medium"
    else:
        category = "bright"

    return {"brightness": round(brightness, 2), "category": category}


def is_infrared_image(image):
    """
    Detects if an image is likely infrared by measuring average saturation (HSV-based).
    """
    threshold = CONFIG["infrared_threshold"]

    image = image.convert("RGB").resize((64, 64))
    pixels = list(image.getdata())

    saturations = []
    for r, g, b in pixels:
        _, s, _ = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        saturations.append(s * 100)

    avg_saturation = sum(saturations) / len(saturations)
    return avg_saturation < threshold


def load_image_from_request(req):
    if req.content_type and req.content_type.startswith("multipart/form-data"):
        if "image" not in req.files:
            raise ValueError("Missing image file")
        return Image.open(req.files["image"].stream)

    if req.is_json:
        data = req.get_json()
        if not data or "url" not in data:
            raise ValueError("Missing 'url'")
        response = requests.get(data["url"], timeout=5)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))

    raise ValueError("Unsupported Content-Type")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        image = load_image_from_request(request)

        brightness_data = analyze_image_brightness(image)
        infrared = is_infrared_image(image)

        return jsonify(
            {
                **brightness_data,
                "is_infrared": infrared,
            }
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to download image: {e}"}), 502
    except Exception as e:
        return jsonify({"error": "Failed to analyze image"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
