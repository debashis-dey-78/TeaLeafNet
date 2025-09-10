import React, { createContext, useContext, useState, ReactNode } from 'react';

export type Screen = 'splash' | 'home' | 'analysis';

interface NavigationContextType {
  currentScreen: Screen;
  navigateTo: (screen: Screen) => void;
  goBack: () => void;
  canGoBack: () => boolean;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

interface NavigationProviderProps {
  children: ReactNode;
}

export const NavigationProvider: React.FC<NavigationProviderProps> = ({ children }) => {
  const [screenHistory, setScreenHistory] = useState<Screen[]>(['splash']);
  const [currentScreen, setCurrentScreen] = useState<Screen>('splash');

  const navigateTo = (screen: Screen) => {
    setScreenHistory(prev => [...prev, screen]);
    setCurrentScreen(screen);
  };

  const goBack = () => {
    if (screenHistory.length > 1) {
      const newHistory = [...screenHistory];
      newHistory.pop(); // Remove current screen
      const previousScreen = newHistory[newHistory.length - 1];
      setScreenHistory(newHistory);
      setCurrentScreen(previousScreen);
    }
  };

  const canGoBack = () => {
    return screenHistory.length > 1 && currentScreen !== 'splash' && currentScreen !== 'home';
  };

  return (
    <NavigationContext.Provider value={{
      currentScreen,
      navigateTo,
      goBack,
      canGoBack,
    }}>
      {children}
    </NavigationContext.Provider>
  );
};

export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (context === undefined) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
};
