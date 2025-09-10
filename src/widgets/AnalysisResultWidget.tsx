import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  TouchableOpacity,
  ScrollView,
} from 'react-native';
import BackButton from './BackButton';
import { AnalysisResult } from '../screens/HomeScreen';

interface AnalysisResultWidgetProps {
  result: AnalysisResult;
  onNewAnalysis: () => void;
}

const diseaseInfo = {
  gl: {
    title: 'Healthy Leaf',
    color: '#4caf50',
    description: 'This is a Non-diseased (Healthy) tea leaf.',
    management: 'No specific management actions are required other than routine good agricultural practices to maintain plant health.',
  },
  rr: {
    title: 'Red Rust',
    color: '#ff9800',
    description: 'Red rust is a common disease of tea plants caused by an alga, Cephaleuros virescens. It appears as orange-brown, velvety patches on leaves.',
    management: '• Improve air circulation by proper pruning and spacing\n• Manage shade to reduce humidity\n• Apply appropriate copper-based fungicides if severe\n• Ensure balanced plant nutrition',
  },
  rsm: {
    title: 'Red Spider Mites',
    color: '#f44336',
    description: 'Red spider mites (Oligonychus coffeae) are common pests that suck sap from tea leaves, leading to reddish-brown discoloration.',
    management: '• Maintain plant vigor through proper irrigation and fertilization\n• Encourage natural predators of mites\n• Use approved miticides if infestation is heavy\n• Regularly monitor for early signs of infestation',
  },
  bb: {
    title: 'Brown Blight',
    color: '#8d6e63',
    description: 'Brown blight, caused by the fungus Colletotrichum spp., leads to distinct brown, often circular lesions on tea leaves.',
    management: '• Prune and destroy affected plant parts\n• Ensure proper plant spacing for air circulation\n• Apply fungicides as recommended by experts\n• Avoid excessive nitrogen fertilization',
  },
};

const AnalysisResultWidget: React.FC<AnalysisResultWidgetProps> = ({ result, onNewAnalysis }) => {
  const { isLeaf, leafConfidence, diseaseClass, diseaseConfidence, imageUri } = result;

  const renderStage1Result = () => (
    <View style={styles.stageContainer}>
      <Text style={styles.stageTitle}>⚙️ Stage 1: Leaf Detection</Text>
      {isLeaf ? (
        <View style={[styles.resultBox, { backgroundColor: '#e8f5e8', borderColor: '#4caf50' }]}>
          <Text style={[styles.resultText, { color: '#2e7d32' }]}>
            ✅ Image identified as a LEAF
          </Text>
          <Text style={styles.confidenceText}>
            Confidence: {leafConfidence.toFixed(2)}%
          </Text>
        </View>
      ) : (
        <View style={[styles.resultBox, { backgroundColor: '#ffebee', borderColor: '#f44336' }]}>
          <Text style={[styles.resultText, { color: '#c62828' }]}>
            ❌ Image does NOT appear to be a leaf
          </Text>
          <Text style={styles.confidenceText}>
            Confidence of being Non-Leaf: {leafConfidence.toFixed(2)}%
          </Text>
        </View>
      )}
    </View>
  );

  const renderStage2Result = () => {
    if (!isLeaf || !diseaseClass || !diseaseConfidence) return null;

    const disease = diseaseInfo[diseaseClass as keyof typeof diseaseInfo];
    const isHealthy = diseaseClass === 'gl';

    return (
      <View style={styles.stageContainer}>
        <Text style={styles.stageTitle}>⚙️ Stage 2: Disease/Pest Detection</Text>
        
        <View style={[styles.resultBox, { 
          backgroundColor: isHealthy ? '#e8f5e8' : '#fff3e0', 
          borderColor: isHealthy ? '#4caf50' : '#ff9800' 
        }]}>
          <Text style={[styles.resultText, { 
            color: isHealthy ? '#2e7d32' : '#e65100' 
          }]}>
            {isHealthy ? 'Status: Healthy Leaf' : `Status: ${diseaseClass.toUpperCase()} (Potential Issue)`}
          </Text>
          
          <View style={styles.progressContainer}>
            <Text style={styles.confidenceText}>
              Confidence: {diseaseConfidence.toFixed(2)}%
            </Text>
            <View style={styles.progressBar}>
              <View style={[
                styles.progressFill, 
                { 
                  width: `${diseaseConfidence}%`,
                  backgroundColor: isHealthy ? '#4caf50' : '#ff9800'
                }
              ]} />
            </View>
          </View>
        </View>

        {disease && (
          <View style={styles.diseaseInfo}>
            <Text style={[styles.diseaseTitle, { color: disease.color }]}>
              {disease.title}
            </Text>
            <Text style={styles.diseaseDescription}>
              {disease.description}
            </Text>
            <Text style={styles.managementTitle}>Management:</Text>
            <Text style={styles.managementText}>
              {disease.management}
            </Text>
          </View>
        )}
      </View>
    );
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      <BackButton />
      <Text style={styles.title}>2. Analysis Results</Text>
      
      <View style={styles.imageContainer}>
        <Image source={{ uri: imageUri }} style={styles.image} />
        <Text style={styles.imageCaption}>Original Input Image</Text>
      </View>

      <View style={styles.divider} />

      {renderStage1Result()}

      {isLeaf && (
        <>
          <View style={styles.divider} />
          {renderStage2Result()}
        </>
      )}

      <TouchableOpacity style={styles.newAnalysisButton} onPress={onNewAnalysis}>
        <Text style={styles.newAnalysisButtonText}>Analyze Another Image</Text>
      </TouchableOpacity>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 10,
    marginBottom: 20,
    color: '#333',
  },
  imageContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  image: {
    width: 200,
    height: 200,
    borderRadius: 10,
    marginBottom: 10,
  },
  imageCaption: {
    fontSize: 14,
    color: '#666',
    fontStyle: 'italic',
  },
  divider: {
    height: 1,
    backgroundColor: '#e0e0e0',
    marginVertical: 20,
  },
  stageContainer: {
    marginBottom: 20,
  },
  stageTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
    color: '#333',
  },
  resultBox: {
    padding: 15,
    borderRadius: 8,
    borderWidth: 2,
    marginBottom: 10,
  },
  resultText: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
  },
  confidenceText: {
    fontSize: 14,
    color: '#666',
  },
  progressContainer: {
    marginTop: 10,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginTop: 5,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  diseaseInfo: {
    backgroundColor: '#f9f9f9',
    padding: 15,
    borderRadius: 8,
    marginTop: 10,
  },
  diseaseTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  diseaseDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 10,
    lineHeight: 20,
  },
  managementTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  managementText: {
    fontSize: 13,
    color: '#666',
    lineHeight: 18,
  },
  newAnalysisButton: {
    backgroundColor: '#2e7d32',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 20,
  },
  newAnalysisButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default AnalysisResultWidget;
