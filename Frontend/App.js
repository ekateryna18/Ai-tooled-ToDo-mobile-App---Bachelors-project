import 'react-native-gesture-handler';
import React, {useState, useEffect} from 'react';
import TaskList from './src/Task/TaskList';
import EditTask from './src/Task/EditTask';
import { TaskProvider } from './src/Task/TaskProvider';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import LoginMain from './src/Login/LoginMain';
import { AuthProvider } from './src/Login/AuthProvider';

var connection_string = "http://192.168.1.197:5000"
const Stack = createStackNavigator();
function App () {

  return (
    <AuthProvider>
      <TaskProvider>
        <NavigationContainer>
          <Stack.Navigator initialRouteName="LoginMain">
            <Stack.Screen name="LoginMain" component={LoginMain} options={{title: "Login"}}/>
            <Stack.Screen name="Main" component={TaskList}  options={{ headerShown: false }}/>
            <Stack.Screen name="EditTask" component={EditTask} options={{title: "Task"}}/>
          </Stack.Navigator>
        </NavigationContainer>
      </TaskProvider>
    </AuthProvider>
  );
};

export default App;
