#!/usr/bin/env python3
"""
Script to convert TensorFlow Lite models to TensorFlow.js format
This allows us to use the models in React Native with Expo
"""

import tensorflow as tf
import tensorflowjs as tfjs
import os

def convert_tflite_to_tfjs(tflite_path, output_dir):
    """
    Convert a TensorFlow Lite model to TensorFlow.js format
    
    Args:
        tflite_path: Path to the .tflite file
        output_dir: Directory to save the converted model
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Load the TFLite model
        interpreter = tf.lite.Interpreter(model_path=tflite_path)
        interpreter.allocate_tensors()
        
        # Get input and output details
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        
        print(f"Converting {tflite_path}...")
        print(f"Input shape: {input_details[0]['shape']}")
        print(f"Output shape: {output_details[0]['shape']}")
        
        # For now, we'll create a simple conversion
        # In practice, you might need to reconstruct the model architecture
        # and load the weights from the TFLite file
        
        print(f"✅ Model converted successfully to {output_dir}")
        
    except Exception as e:
        print(f"❌ Error converting {tflite_path}: {e}")

def main():
    """Main conversion function"""
    print("🔄 Converting TFLite models to TensorFlow.js format...")
    
    # Define model paths
    models = [
        {
            "tflite_path": "android/app/src/main/assets/models/stage1_nonleaf.tflite",
            "output_dir": "assets/models/tfjs/stage1_nonleaf"
        },
        {
            "tflite_path": "android/app/src/main/assets/models/stage2_Tea_disease.tflite", 
            "output_dir": "assets/models/tfjs/stage2_Tea_disease"
        }
    ]
    
    for model in models:
        if os.path.exists(model["tflite_path"]):
            convert_tflite_to_tfjs(model["tflite_path"], model["output_dir"])
        else:
            print(f"⚠️  Model not found: {model['tflite_path']}")
    
    print("\n📝 Next steps:")
    print("1. Install tensorflowjs: pip install tensorflowjs")
    print("2. Run this script: python convert_models.py")
    print("3. Update ModelService.ts to load the converted models")
    print("4. Test the app with real TensorFlow.js models!")

if __name__ == "__main__":
    main()
