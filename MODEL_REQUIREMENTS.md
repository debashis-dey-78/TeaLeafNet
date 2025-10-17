# TeaLeafNet Model Requirements

## Model Specifications

### Stage 1: Leaf Detection Model (`stage1_nonleaf.tflite`)
- **Input Size**: 160x160 pixels
- **Channels**: 3 (RGB)
- **Input Shape**: [1, 160, 160, 3]
- **Normalization**: `rescale=1./255` (matches `train_datagen = ImageDataGenerator(rescale=1./255)`)
- **Purpose**: Determines if the input image contains a tea leaf or not

### Stage 2: Disease Classification Model (`stage2_Tea_disease.tflite`)
- **Input Size**: 512x512 pixels
- **Channels**: 3 (RGB)
- **Input Shape**: [1, 512, 512, 3]
- **Normalization**: `x_train / 255.0` (matches training code)
- **Purpose**: Classifies tea leaf diseases into 4 classes

## Preprocessing Pipeline

### Image Processing Steps
1. **Load Image**: Read image from URI (camera or gallery)
2. **Resize**: Resize to model-specific dimensions
   - Stage 1: 160x160
   - Stage 2: 512x512
3. **Normalize**: Divide pixel values by 255.0 to get range [0, 1]
4. **Add Batch Dimension**: Shape becomes [1, height, width, 3]
5. **Model Inference**: Pass to respective TensorFlow Lite model

### Normalization Details
Both models expect the same normalization:
```python
# Stage 1 (from training)
train_datagen = ImageDataGenerator(rescale=1./255)

# Stage 2 (from training)
x_train = np.array(x_train, dtype=np.float16) / 255.0
```

**JavaScript Implementation**:
```typescript
// Both models use the same normalization
const normalized = resized.div(255.0);
```

## Model Classes

### Stage 1 Output
- **Binary Classification**: Leaf (1) or Non-leaf (0)
- **Confidence Score**: Probability of being a leaf

### Stage 2 Output (4 Disease Classes)
- **gl**: Healthy (Green Leaf)
- **rr**: Red Rust
- **rsm**: Red Spider Mites
- **bb**: Brown Blight

## Implementation Status

### ✅ Completed
- Model-specific input size handling
- Proper normalization implementation
- Two-stage preprocessing pipeline
- Comprehensive logging and verification
- TensorFlow.js integration ready

### 🔄 Ready for Production
- When TensorFlow Lite models are loaded, the preprocessing is already correctly implemented
- Both models will receive properly sized and normalized input tensors
- All logging shows the correct model requirements and verification

## Usage in App

The app automatically:
1. Preprocesses images for Stage 1 (160x160) for leaf detection
2. If leaf detected, preprocesses same image for Stage 2 (512x512) for disease classification
3. Both stages use identical normalization (divide by 255.0)
4. Results are displayed with confidence scores and management recommendations
