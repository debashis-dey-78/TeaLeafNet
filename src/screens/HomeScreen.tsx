import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  SafeAreaView,
  Alert,
} from 'react-native';
import ImagePickerWidget from '../widgets/ImagePickerWidget';
import AnalysisResultWidget from '../widgets/AnalysisResultWidget';
import LoadingWidget from '../widgets/LoadingWidget';
import BackButton from '../widgets/BackButton';
import { ModelService } from '../services/ModelService';
import { useNavigation } from '../contexts/NavigationContext';

export interface AnalysisResult {
  isLeaf: boolean;
  leafConfidence: number;
  diseaseClass?: string;
  diseaseConfidence?: number;
  imageUri: string;
}

const HomeScreen: React.FC = () => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [modelService] = useState(() => new ModelService());
  const { navigateTo } = useNavigation();

  const handleImageSelected = async (imageUri: string) => {
    setSelectedImage(imageUri);
    setAnalysisResult(null);
    setIsAnalyzing(true);
    navigateTo('analysis');

    try {
      const result = await modelService.analyzeImage(imageUri);
      setAnalysisResult(result);
    } catch (error) {
      console.error('Analysis error:', error);
      Alert.alert(
        'Analysis Error',
        'Failed to analyze the image. Please try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleNewAnalysis = () => {
    setSelectedImage(null);
    setAnalysisResult(null);
    navigateTo('home');
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <View style={styles.header}>
          <BackButton />
          <Text style={styles.title}>🌿 TeaLeafNet</Text>
          <Text style={styles.subtitle}>
            Upload an image of a tea leaf. The system will first check if it's a valid leaf image and then identify potential diseases or pests.
          </Text>
        </View>

        <View style={styles.content}>
          {!selectedImage ? (
            <ImagePickerWidget onImageSelected={handleImageSelected} />
          ) : (
            <View style={styles.analysisContainer}>
              {isAnalyzing ? (
                <LoadingWidget />
              ) : analysisResult ? (
                <AnalysisResultWidget
                  result={analysisResult}
                  onNewAnalysis={handleNewAnalysis}
                />
              ) : null}
            </View>
          )}
        </View>

        <View style={styles.footer}>
          <Text style={styles.footerText}>Developed by Harjinder Singh</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContent: {
    flexGrow: 1,
  },
  header: {
    padding: 20,
    paddingTop: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#e0e0e0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 15,
    marginBottom: 12,
    color: '#2e7d32',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    color: '#666',
    lineHeight: 22,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  analysisContainer: {
    flex: 1,
  },
  footer: {
    padding: 20,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#999',
  },
});

export default HomeScreen;
