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
        result = analyze_image_brightness(image)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
