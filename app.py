from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import os
import gdown  # Import gdown for downloading files

app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend requests

# 🔹 Google Drive File ID (Replace with your own)
file_id = "1y5q7wZ93f1VPqvgLVCxRIN6kR9kCzmEj"

# 🔹 Model path
model_path = "resnet_model.h5"

# ✅ Download model if not available locally
if not os.path.exists(model_path):
    print("🔽 Downloading ResNet model from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", model_path, quiet=False)
    print("✅ Download complete!")

# ✅ Load the trained ResNet model
print("🔄 Loading model...")
model = keras.models.load_model(model_path)
print("✅ Model loaded successfully!")

# Function to preprocess uploaded image
def preprocess_image(image):
    image = image.resize((224, 224))  # Resize for ResNet input
    image = np.array(image) / 255.0   # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recommendations')
def recommendations():
    return render_template('recommendations.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = Image.open(file).convert("RGB")  # Ensure 3-channel image
        processed_image = preprocess_image(image)
        
        # 🔹 Make prediction
        prediction = model.predict(processed_image)
        predicted_class = "Osteoporosis Detected" if prediction[0][0] > 0.5 else "Normal Bone"

        return jsonify({"prediction": predicted_class})
    
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Default to 10000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
