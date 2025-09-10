# TeaLeafNet - React Native App

A React Native app for tea leaf disease detection using TensorFlow.js. The app performs two-stage analysis: first detecting if an image contains a leaf, then classifying any diseases or pests.

## Features

- **Two-Stage Analysis**: 
  - Stage 1: Leaf vs Non-leaf detection
  - Stage 2: Disease classification (4 classes: Healthy, Red Rust, Red Spider Mites, Brown Blight)
- **Camera Integration**: Take photos directly with your device
- **Gallery Support**: Select images from your photo library
- **Offline Operation**: No internet required (when models are integrated)
- **Real-time Results**: Instant analysis with confidence scores
- **Management Recommendations**: Detailed disease information and treatment advice

## Quick Start

### Prerequisites

1. **Node.js** (v18 or higher)
2. **Expo CLI**: `npm install -g @expo/cli`
3. **Expo Go app** on your Android phone (download from Google Play Store)

### Installation

1. **Install dependencies:**
   ```bash
   npm install --legacy-peer-deps
   ```

2. **Start the development server:**
   ```bash
   npx expo start
   ```

3. **Run on your Android phone:**
   - Open Expo Go app on your phone
   - Scan the QR code displayed in your terminal/browser
   - The app will load on your phone

## Model Files

The app requires two TensorFlow Lite model files placed in the `assets/models/` directory:

- `stage1_nonleaf.tflite` - Leaf detection model (~18MB)
- `stage2_Tea_disease.tflite` - Disease classification model (~137MB)

**Model files are already in place at:** `assets/models/`

## Project Structure

```
TeaLeafNet/
├── App.tsx                          # Main app component
├── src/
│   ├── screens/
│   │   └── HomeScreen.tsx           # Main screen with image picker and analysis
│   ├── widgets/
│   │   ├── ImagePickerWidget.tsx    # Camera and gallery image selection
│   │   ├── AnalysisResultWidget.tsx # Disease analysis results display
│   │   └── LoadingWidget.tsx        # Loading indicator component
│   └── services/
│       └── ModelService.ts          # TensorFlow.js model handling
├── assets/
│   └── models/                      # TensorFlow Lite model files
│       ├── stage1_nonleaf.tflite    # Leaf detection model
│       └── stage2_Tea_disease.tflite # Disease classification model
├── app.json                         # Expo configuration
├── package.json                     # Dependencies
└── tsconfig.json                    # TypeScript configuration
```

## Current Status

This is a **demo version** with mock analysis results. The app includes:

✅ Complete UI implementation
✅ Image picker (camera + gallery)
✅ Two-stage analysis flow
✅ Disease information display
✅ Responsive design
✅ TypeScript support
✅ Model file loading (assets loaded, ready for TensorFlow.js integration)

🔄 **To be implemented:**
- Actual TensorFlow.js model inference
- Real image preprocessing for model input

## Model Integration Status

The app is configured to load model files from `assets/models/` directory:

- ✅ Model files are in place
- ✅ Asset loading is implemented
- ✅ Model paths are correctly referenced
- 🔄 TensorFlow.js inference (ready for implementation)

## Dependencies

- **Expo**: ~49.0.0
- **React Native**: 0.72.10
- **TensorFlow.js**: ^4.15.0
- **Expo Image Picker**: ~14.3.2
- **Expo Camera**: ~13.4.4

## Development

The app uses Expo for easy development and deployment. Key features:

- **Hot Reload**: Changes reflect immediately
- **Cross-platform**: Works on Android and iOS
- **TypeScript**: Full type safety
- **Modern React**: Hooks and functional components

## Troubleshooting

### Common Issues

1. **Metro bundler issues**: Clear cache with `npx expo start --clear`
2. **Permission errors**: Make sure camera and photo library permissions are granted
3. **Build errors**: Try `npm install --legacy-peer-deps` and `npx expo start --clear`

### Getting Help

- Check the [Expo documentation](https://docs.expo.dev/)
- Review the [React Native documentation](https://reactnative.dev/)
- Check the [TensorFlow.js documentation](https://www.tensorflow.org/js)

## License

Developed by Harjinder Singh
