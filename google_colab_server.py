#!/usr/bin/env python3
"""
TeaLeafNet TFLite Model Server for Google Colab
This script runs your TFLite models and provides a public API via ngrok
"""

# Install required packages (run this first in Colab)
# !pip install flask flask-cors tensorflow pillow
# !wget -q -c -nc https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
# !unzip -o -q ngrok-stable-linux-amd64.zip

import tensorflow as tf
import numpy as np
from PIL import Image
import io
import base64
import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import threading
import time

class TeaLeafModel:
    def __init__(self):
        self.leaf_interpreter = None
        self.disease_interpreter = None
        self.disease_classes = ['bb', 'gl', 'rr', 'rsm']
        self.load_models()
    
    def load_models(self):
        """Load TFLite models"""
        try:
            # Create models directory
            os.makedirs('models', exist_ok=True)
            
            # Download models from Hugging Face
            self.download_models()
            
            # Load leaf detection model
            self.leaf_interpreter = tf.lite.Interpreter(model_path='models/leaf_detection.tflite')
            self.leaf_interpreter.allocate_tensors()
            
            # Load disease classification model
            self.disease_interpreter = tf.lite.Interpreter(model_path='models/disease_classification.tflite')
            self.disease_interpreter.allocate_tensors()
            
            print("✅ TFLite models loaded successfully!")
            self.print_model_info()
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise e
    
    def download_models(self):
        """Download TFLite models from Hugging Face"""
        models = {
            'leaf_detection.tflite': 'https://huggingface.co/kd8811/TeaLeafNet/resolve/main/leaf_detection.tflite',
            'disease_classification.tflite': 'https://huggingface.co/kd8811/TeaLeafNet/resolve/main/disease_classification.tflite'
        }
        
        for filename, url in models.items():
            if not os.path.exists(f'models/{filename}'):
                print(f"Downloading {filename}...")
                response = requests.get(url)
                with open(f'models/{filename}', 'wb') as f:
                    f.write(response.content)
                print(f"✅ {filename} downloaded successfully!")
    
    def print_model_info(self):
        """Print model input/output details"""
        print("\n📊 Model Information:")
        
        # Leaf detection model info
        leaf_input = self.leaf_interpreter.get_input_details()[0]
        leaf_output = self.leaf_interpreter.get_output_details()[0]
        print(f"Leaf Detection - Input: {leaf_input['shape']}, Output: {leaf_output['shape']}")
        
        # Disease classification model info
        disease_input = self.disease_interpreter.get_input_details()[0]
        disease_output = self.disease_interpreter.get_output_details()[0]
        print(f"Disease Classification - Input: {disease_input['shape']}, Output: {disease_output['shape']}")
    
    def preprocess_image(self, image_base64, target_size):
        """Preprocess image for model input"""
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            
            # Resize image
            image = image.resize(target_size)
            
            # Convert to numpy array and normalize
            image_array = np.array(image, dtype=np.float32) / 255.0
            
            # Add batch dimension
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            raise e
    
    def detect_leaf(self, image_base64):
        """Stage 1: Detect if image contains a tea leaf"""
        try:
            # Preprocess image for leaf detection (160x160)
            input_data = self.preprocess_image(image_base64, (160, 160))
            
            # Run inference
            self.leaf_interpreter.set_tensor(self.leaf_interpreter.get_input_details()[0]['index'], input_data)
            self.leaf_interpreter.invoke()
            
            # Get output
            output = self.leaf_interpreter.get_tensor(self.leaf_interpreter.get_output_details()[0]['index'])
            
            # Process result (assuming output is probability of non-leaf)
            non_leaf_prob = float(output[0][0])
            is_leaf = non_leaf_prob <= 0.5
            confidence = (1 - non_leaf_prob) if is_leaf else non_leaf_prob
            
            return {
                'isLeaf': is_leaf,
                'confidence': float(confidence)
            }
            
        except Exception as e:
            print(f"❌ Error in leaf detection: {e}")
            return {'isLeaf': False, 'confidence': 0.0}
    
    def classify_disease(self, image_base64):
        """Stage 2: Classify tea leaf disease"""
        try:
            # Preprocess image for disease classification (512x512)
            input_data = self.preprocess_image(image_base64, (512, 512))
            
            # Run inference
            self.disease_interpreter.set_tensor(self.disease_interpreter.get_input_details()[0]['index'], input_data)
            self.disease_interpreter.invoke()
            
            # Get output
            output = self.disease_interpreter.get_tensor(self.disease_interpreter.get_output_details()[0]['index'])
            
            # Process result
            probabilities = output[0]
            predicted_class_idx = np.argmax(probabilities)
            predicted_class = self.disease_classes[predicted_class_idx]
            confidence = float(probabilities[predicted_class_idx])
            
            return {
                'class': predicted_class,
                'confidence': confidence
            }
            
        except Exception as e:
            print(f"❌ Error in disease classification: {e}")
            return {'class': 'bb', 'confidence': 0.0}
    
    def analyze_image(self, image_base64):
        """Complete analysis pipeline"""
        try:
            print("🔍 Starting image analysis...")
            
            # Stage 1: Leaf Detection
            leaf_result = self.detect_leaf(image_base64)
            print(f"Stage 1 - Leaf detected: {leaf_result['isLeaf']} (confidence: {leaf_result['confidence']:.3f})")
            
            disease_result = None
            if leaf_result['isLeaf']:
                # Stage 2: Disease Classification
                disease_result = self.classify_disease(image_base64)
                print(f"Stage 2 - Disease: {disease_result['class']} (confidence: {disease_result['confidence']:.3f})")
            
            return {
                'isLeaf': leaf_result['isLeaf'],
                'leafConfidence': leaf_result['confidence'],
                'diseaseClass': disease_result['class'] if disease_result else None,
                'diseaseConfidence': disease_result['confidence'] if disease_result else None
            }
            
        except Exception as e:
            print(f"❌ Error in complete analysis: {e}")
            return {
                'isLeaf': False,
                'leafConfidence': 0.0,
                'diseaseClass': None,
                'diseaseConfidence': None
            }

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the model
print("🤖 Initializing TFLite models...")
model = TeaLeafModel()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'TeaLeafNet TFLite API',
        'models_loaded': model.leaf_interpreter is not None and model.disease_interpreter is not None
    })

@app.route('/analyze', methods=['POST'])
def analyze_image():
    """Analyze tea leaf image"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400
        
        image_base64 = data['image']
        
        # Analyze image with TFLite models
        result = model.analyze_image(image_base64)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint with sample data"""
    return jsonify({
        'message': 'TeaLeafNet TFLite API is running!',
        'endpoints': ['/health', '/analyze', '/test'],
        'status': 'ready'
    })

def start_ngrok():
    """Start ngrok tunnel"""
    try:
        # Start ngrok on port 5000
        subprocess.run(['./ngrok', 'http', '5000', '--log=stdout'], check=True)
    except Exception as e:
        print(f"❌ Error starting ngrok: {e}")

def get_ngrok_url():
    """Get ngrok public URL"""
    try:
        response = requests.get('http://localhost:4040/api/tunnels')
        tunnels = response.json()['tunnels']
        
        if tunnels:
            return tunnels[0]['public_url']
        else:
            return None
    except Exception as e:
        print(f"❌ Error getting ngrok URL: {e}")
        return None

if __name__ == '__main__':
    print("\n🎉 TeaLeafNet TFLite API Server Starting...")
    
    # Start ngrok in background
    print("🌍 Starting ngrok tunnel...")
    ngrok_thread = threading.Thread(target=start_ngrok, daemon=True)
    ngrok_thread.start()
    
    # Wait for ngrok to start
    time.sleep(5)
    
    # Get ngrok URL
    ngrok_url = get_ngrok_url()
    if ngrok_url:
        print(f"🌍 Your API is now public at: {ngrok_url}")
        print(f"📋 Health check: {ngrok_url}/health")
        print(f"🔍 Test endpoint: {ngrok_url}/test")
        print(f"\n📱 Update your React Native app with this URL:")
        print(f"API_BASE_URL = '{ngrok_url}'")
    else:
        print("❌ Could not get ngrok URL. Check manually at http://localhost:4040")
    
    print("\n🚀 Starting Flask server...")
    print("📱 Your React Native app can now connect to this API!")
    print("\n⚠️  Keep this running to keep the API alive")
    print("⚠️  Don't close this or the API will stop")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
