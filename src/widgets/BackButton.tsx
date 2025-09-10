import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
} from 'react-native';
import { useNavigation } from '../contexts/NavigationContext';

const BackButton: React.FC = () => {
  const { goBack, canGoBack } = useNavigation();

  if (!canGoBack()) {
    return null;
  }

  return (
    <TouchableOpacity style={styles.button} onPress={goBack}>
      <Text style={styles.icon}>←</Text>
      <Text style={styles.text}>Back</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: '#f5f5f5',
    borderRadius: 20,
    marginBottom: 15,
    marginTop: 10,
    alignSelf: 'flex-start',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  icon: {
    fontSize: 18,
    color: '#2e7d32',
    marginRight: 4,
  },
  text: {
    fontSize: 16,
    color: '#2e7d32',
    fontWeight: '500',
  },
});

export default BackButton;
