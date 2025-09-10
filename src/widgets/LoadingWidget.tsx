import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';

const LoadingWidget: React.FC = () => {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#2e7d32" />
      <Text style={styles.text}>Analyzing image...</Text>
      <Text style={styles.subtext}>This may take a few moments</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  text: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginTop: 20,
    marginBottom: 8,
  },
  subtext: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
});

export default LoadingWidget;
