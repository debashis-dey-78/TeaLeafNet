# TeaLeafNet - React Native Setup Instructions

## Prerequisites

1. **Node.js** (v20 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **React Native CLI**
   - Install globally: `npm install -g @react-native-community/cli`

3. **Android Studio** (for Android development)
   - Download from: https://developer.android.com/studio
   - Install Android SDK and emulator

4. **Xcode** (for iOS development - macOS only)
   - Download from Mac App Store

## Setup Steps

### 1. Install Dependencies
Open Command Prompt/Terminal in the project directory and run:
```bash
npm install
```

### 2. Android Setup
**Detailed Android setup instructions are available in [ANDROID_SETUP.md](./ANDROID_SETUP.md)**

Quick setup:
1. Install Android Studio and Android SDK
2. Set ANDROID_HOME environment variable
3. Create `android/local.properties` file with SDK path
4. Create Android Virtual Device (AVD) or connect physical device
5. Enable USB Debugging on your device

### 3. iOS Setup (macOS only)
1. Navigate to the ios directory: `cd ios`
2. Install CocoaPods dependencies: `pod install`
3. Return to project root: `cd ..`

### 4. Run the App

**For Android:**
```bash
npx react-native run-android
```

**For iOS (macOS only):**
```bash
npx react-native run-ios
```

**Start Metro bundler separately:**
```bash
npx react-native start
```

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
│       ├── stage1_nonleaf.tflite    # Leaf detection model (~18MB)
│       └── stage2_Tea_disease.tflite # Disease classification model (~137MB)
├── android/                         # Android configuration
└── ios/                            # iOS configuration
```

## Features

- **Offline Operation**: No internet required
- **Two-Stage Analysis**: 
  - Stage 1: Leaf vs Non-leaf detection
  - Stage 2: Disease classification (4 classes)
- **Camera Integration**: Take photos directly
- **Gallery Support**: Select from existing images
- **Real-time Results**: Instant analysis with confidence scores
- **Management Recommendations**: Detailed disease information

## Dependencies

- **React Native**: 0.81.1
- **TensorFlow.js**: 4.22.0
- **React Native Image Picker**: 8.2.1
- **React Native Permissions**: 5.4.2

## Troubleshooting

### Metro Bundler Issues
- Clear cache: `npx react-native start --reset-cache`
- Clean project: `npx react-native clean`

### Android Issues
- Check if device is connected: `adb devices`
- Restart ADB: `adb kill-server && adb start-server`
- Clean Android build: `cd android && ./gradlew clean && cd ..`

### iOS Issues
- Clean build folder in Xcode
- Reset iOS simulator: Device > Erase All Content and Settings
- Reinstall pods: `cd ios && pod install && cd ..`

### General Issues
- Clear npm cache: `npm cache clean --force`
- Delete node_modules: `rm -rf node_modules && npm install`
- Check React Native version compatibility

## Model Files

The app requires two TensorFlow Lite model files:
1. `stage1_nonleaf.tflite` - Leaf detection model
2. `stage2_Tea_disease.tflite` - Disease classification model

Place these files in the `assets/models/` directory. The models are not included in the repository due to their large size (~155MB total).

## Development Notes

- The app uses mock data for analysis results until the actual models are integrated
- TensorFlow.js is configured for React Native with platform-specific optimizations
- Camera and storage permissions are configured for both Android and iOS
- The app follows React Native best practices with TypeScript

## Support

For issues or questions, check the React Native documentation or contact the developer.