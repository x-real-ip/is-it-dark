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
    brightness = sum(i * histo for i, histo in enumerate(histogram)) / pixels

    dark_thresh = CONFIG["brightness_thresholds"]["dark"]
    medium_thresh = CONFIG["brightness_thresholds"]["medium"]

    if brightness < dark_thresh:
        category = "dark"
    elif brightness < medium_thresh:
        category = "medium"
    else:
        category = "bright"

    return {
        "brightness": round(brightness, 2),
        "category": category
    }


def is_infrared_image(image):
    """
    Detects if an image is likely infrared by measuring average saturation (HSV-based).
    """
    threshold = CONFIG["infrared_threshold"]
    image = image.convert("RGB").resize((64, 64))  # Resize for performance
    pixels = list(image.getdata())

    saturations = []
    for r, g, b in pixels:
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        saturations.append(s * 100)  # Convert to 0–100 range

    avg_saturation = sum(saturations) / len(saturations)
    return avg_saturation < threshold


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url'"}), 400

    try:
        response = requests.get(data['url'], timeout=5)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
    except Exception as e:
        return jsonify({"error": f"Failed to download image: {str(e)}"}), 500

    try:
        brightness_data = analyze_image_brightness(image)
        infrared = is_infrared_image(image)

        return jsonify({
            **brightness_data,
            "is_infrared": infrared
        })
    except Exception as e:
        return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
