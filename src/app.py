from flask import Flask, request, jsonify
from PIL import Image
import requests
import io

app = Flask(__name__)


def analyze_image_brightness(image):
    grayscale = image.convert("L")
    histogram = grayscale.histogram()
    pixels = sum(histogram)
    brightness = sum(i * histo for i, histo in enumerate(histogram)) / pixels

    # Categorize based on thresholds
    if brightness < 50:
        category = "dark"
    elif brightness < 170:
        category = "medium"
    else:
        category = "bright"

    return {
        "brightness": round(brightness, 2),
        "category": category
    }


def is_infrared_image(image, threshold=15):
    image = image.convert("RGB")
    pixels = list(image.getdata())

    def rgb_to_saturation(r, g, b):
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        if max_val == 0:
            return 0
        return (max_val - min_val) / max_val * 100

    saturations = [rgb_to_saturation(r, g, b) for r, g, b in pixels]
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
