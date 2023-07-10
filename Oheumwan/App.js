import * as React from 'react';
import { Text, View, StyleSheet } from 'react-native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { NavigationContainer } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { WebView } from 'react-native-webview';

const Tab = createBottomTabNavigator();

const ScreenOptions = ({ route }) => ({
  tabBarIcon: ({ focused, color, size }) => {
    let iconName;
    switch (route.name) {
      case 'Home':
        iconName = focused ? 'home' : 'home-outline';
        break;
      case 'Community':
        iconName = focused ? 'heart' : 'heart-outline';
        break;
      case 'Add':
        iconName = focused ? 'add-circle' : 'add-circle-outline';
        break;
      case 'Feed':
        iconName = focused ? 'person' : 'person-outline';
        break;
      case 'Setting':
        iconName = focused ? 'settings' : 'settings-outline';
        break;
      default:
        iconName = focused ? 'home' : 'home-outline';
    }
    return <Ionicons name={iconName} size={size} color={color} />;
  },
});

const TabNavigator = () => (
  <Tab.Navigator
    screenOptions={ScreenOptions}
    tabBarOptions={{
      activeTintColor: 'black',
      inactiveTintColor: 'gray',
      showLabel: false,
    }}
  >
    <Tab.Screen name="Home" component={HomeScreen} />
    <Tab.Screen name="Community" component={CommunityScreen} />
    <Tab.Screen name="Add" component={AddScreen} />
    <Tab.Screen name="Feed" component={FeedScreen} />
    <Tab.Screen name="Setting" component={SettingScreen} />
  </Tab.Navigator>
);

const HomeScreen = () => (
  <WebView
      style={styles.container}
      source={{ uri: 'https://naver.com' }}
  />
);

const CommunityScreen = () => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Text>Community Screen</Text>
  </View>
);

const AddScreen = () => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Text>CameraApp</Text>
  </View>
);

const FeedScreen = () => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Text>Feed Screen</Text>
  </View>
);

const SettingScreen = () => (
  <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    <Text>Setting Screen</Text>
  </View>
);

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default function App() {
  return (
    <NavigationContainer>
      <TabNavigator />
    </NavigationContainer>
  );
}
