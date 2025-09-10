import React, { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { NavigationProvider, useNavigation } from './src/contexts/NavigationContext';
import SplashScreen from './src/screens/SplashScreen';
import HomeScreen from './src/screens/HomeScreen';

const AppContent: React.FC = () => {
  const { currentScreen, navigateTo } = useNavigation();

  const handleSplashFinish = () => {
    navigateTo('home');
  };

  if (currentScreen === 'splash') {
    return <SplashScreen onFinish={handleSplashFinish} />;
  }

  return <HomeScreen />;
};

export default function App() {
  return (
    <NavigationProvider>
      <StatusBar style="auto" />
      <AppContent />
    </NavigationProvider>
  );
}
