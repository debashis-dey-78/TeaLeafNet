#!/usr/bin/env python3
"""
Convert TensorFlow Lite models to ONNX format for Hugging Face
"""

import tensorflow as tf
import tf2onnx
import onnx
import numpy as np
import os

def convert_tflite_to_onnx(tflite_path, onnx_path, input_shape):
    """
    Convert TensorFlow Lite model to ONNX format
    """
    print(f"Converting {tflite_path} to {onnx_path}...")
    
    # Load TFLite model
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    
    # Get input and output details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    print(f"Input shape: {input_details[0]['shape']}")
    print(f"Output shape: {output_details[0]['shape']}")
    
    # Create a dummy input for conversion
    dummy_input = np.random.randn(1, *input_shape).astype(np.float32)
    
    # Convert to ONNX
    try:
        # This is a simplified conversion - you might need to adjust based on your model
        onnx_model = tf2onnx.convert.from_tflite(
            tflite_path,
            inputs_as_nchw=['input'],  # Adjust based on your model
            output_path=onnx_path
        )
        print(f"✅ Successfully converted to {onnx_path}")
        return True
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def create_model_card(model_name, description, input_shape, output_classes):
    """
    Create a model card for Hugging Face
    """
    card_content = f"""---
license: mit
tags:
- image-classification
- tea-disease-detection
- plant-disease
- computer-vision
---

# {model_name}

{description}

## Model Description

This model detects tea leaf diseases from images.

### Input
- **Image size:** {input_shape[0]}x{input_shape[1]} pixels
- **Format:** RGB image
- **Preprocessing:** Resize to {input_shape[0]}x{input_shape[1]}, normalize to [0,1]

### Output
- **Classes:** {', '.join(output_classes)}
- **Format:** Probability scores for each class

## Usage

```python
from transformers import pipeline

# Load the model
classifier = pipeline("image-classification", model="your-username/{model_name}")

# Classify an image
result = classifier("path/to/tea_leaf_image.jpg")
print(result)
```

## Training Data

This model was trained on tea leaf disease dataset.

## Performance

- **Accuracy:** [To be filled]
- **Precision:** [To be filled]
- **Recall:** [To be filled]

## Limitations

- Works best with clear, well-lit images
- May not perform well on heavily damaged leaves
- Requires proper preprocessing for optimal results
"""
    
    with open(f"{model_name}_README.md", "w") as f:
        f.write(card_content)
    
    print(f"✅ Created model card: {model_name}_README.md")

if __name__ == "__main__":
    # Convert Stage 1: Leaf Detection
    convert_tflite_to_onnx(
        "stage1_nonleaf.tflite",
        "leaf_detection.onnx",
        [160, 160, 3]  # Adjust based on your model
    )
    
    # Convert Stage 2: Disease Classification
    convert_tflite_to_onnx(
        "stage2_Tea_disease.tflite",
        "disease_classification.onnx",
        [512, 512, 3]  # Adjust based on your model
    )
    
    # Create model cards
    create_model_card(
        "tea-leaf-detection",
        "Detects if an image contains a tea leaf or not",
        [160, 160, 3],
        ["non-leaf", "leaf"]
    )
    
    create_model_card(
        "tea-disease-classification",
        "Classifies tea leaf diseases",
        [512, 512, 3],
        ["bb", "gl", "rr", "rsm"]
    )
    
    print("\n🎉 Conversion complete!")
    print("Next steps:")
    print("1. Install required packages: pip install tensorflow tf2onnx onnx")
    print("2. Run this script: python convert_models_for_hf.py")
    print("3. Upload the .onnx files to Hugging Face")
