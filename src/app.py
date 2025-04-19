from flask import Flask, request, jsonify
from PIL import Image
import requests
import io

app = Flask(__name__)

def is_dark_image(image):
    grayscale = image.convert("L")  # Grayscale
    histogram = grayscale.histogram()
    pixels = sum(histogram)
    brightness = sum(i * histo for i, histo in enumerate(histogram)) / pixels
    return brightness < 150  # Adjust this threshold as needed

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
        result = is_dark_image(image)
        return jsonify({"is_dark": result})
    except Exception as e:
        return jsonify({"error": f"Failed to analyze image: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
