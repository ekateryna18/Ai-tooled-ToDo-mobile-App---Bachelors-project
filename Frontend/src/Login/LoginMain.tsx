import React, { useEffect, useState } from 'react';
import { View, Text, SafeAreaView,StyleSheet, TextInput, TouchableOpacity, Alert } from 'react-native';
import { useLogin } from './AuthProvider';

const LoginMain = ({route, navigation}) => {
    const [username, setUsername] = useState('');
    const [password,setPassword] = useState('');
    const {isAuthenticated, login, loginError, register,registerError, isRegistered} = useLogin();
    const [buttonPresssed, setButtonPressed] = useState(0);

    const handleLogin = () => {
      console.log(username + " "+ password);
      login(username, password);
      setButtonPressed(prevIsChanged => prevIsChanged + 1);
    }
    const handleRegister = () => {
      console.log(username + " "+ password);
      register(username, password);
      //setButtonPressed(prevIsChanged => prevIsChanged + 1);
    }
    useEffect(() => {
      if (isAuthenticated) {
        navigation.navigate("Main");
      }
    }, [isAuthenticated]);

    useEffect(() => {
      if (isRegistered) {
        alertSuccesfulRegister();
      }
    }, [isRegistered]);
    const alertFailedLogin = () => Alert.alert('Failed login', 'Wrong password or username',[
      {
        text: 'OK'
      }
    ]);
    const alertFailedRegister = () => Alert.alert('Failed register', 'Username already in use',[
      {
        text: 'OK'
      }
    ]);
    const alertSuccesfulRegister = () => Alert.alert('Successful register', 'Account created!',[
      {
        text: 'OK'
      }
    ]);
    useEffect(() => {
      if (loginError > 0) {
        alertFailedLogin();
      }
    }, [loginError]);

    useEffect(() => {
      if (registerError > 0) {
        alertFailedRegister();
      }
    }, [registerError]);
    return (
        <SafeAreaView style={styles.centeredView}>
          <View >
            <View style={styles.modalView}>
                <TextInput
                  style={styles.input}
                  onChangeText={setUsername}
                  value={username}
                  placeholder="Username"
                  keyboardType="default"
                />
                <TextInput
                  style={styles.input}
                  onChangeText={setPassword}
                  value={password}
                  placeholder="Password"
                  keyboardType="default"
                  secureTextEntry={true}
                />
              <TouchableOpacity style={styles.button} onPress={handleLogin} >
                <Text style={styles.text}>Login</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.button} onPress={handleRegister} >
                <Text style={styles.text}>Register</Text>
              </TouchableOpacity>
            </View>
          </View>
        </SafeAreaView>
      );
};

const styles = StyleSheet.create({
  centeredView: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#86B6F6',
  },
  modalView: {
    margin: 20,
    backgroundColor: "white",
    borderRadius: 20,
    padding: 35,
    alignItems: "center",
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5
  },
  input: {
    height: 40,
    borderWidth: 1,
    padding: 10,
    width: 170,
    borderRadius: 5,
    margin:20,
  },
  button: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 12,
    paddingHorizontal: 32,
    borderRadius: 4,
    elevation: 3,
    backgroundColor: '#3c8dfa',
    marginBottom: 20,
  },
  text: {
    fontSize: 16,
    lineHeight: 21,
    fontWeight: 'bold',
    letterSpacing: 0.25,
    color: 'white',
  },
});
export default LoginMain;