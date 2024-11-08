import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { getLogger } from '../../core';
import {login as loginApi, register as registerApi} from './loginApi';
import AsyncStorage from '@react-native-async-storage/async-storage';

const log = getLogger('AuthProvider');

type LoginFn = (username?: string, password?: string) => void;
type RegisterFn = (username?: string, password?: string) => void;
type LogoutFn = () => void;

export interface AuthState {
  isAuthenticated: boolean;
  loginError? : number;
  registerError? : number;
  username?: string;
  password?: string;
  login?: LoginFn;
  logout?: LogoutFn;
  register?: RegisterFn;
  isRegistered: boolean;
}

const initialState: AuthState = {
    isAuthenticated: false,
    username: '',
    loginError: 0,
    registerError : 0,
    isRegistered:false,
};

const AuthContext = createContext<AuthState>(initialState);
export const useLogin = () => useContext(AuthContext);

export const AuthProvider = ({children}) => {
    const [state, setState] = useState<AuthState>(initialState);
    //const [username, setUsername] = useState('');
    const {isAuthenticated, username, loginError,registerError,isRegistered} = state;
    const login = useCallback<LoginFn>(loginCallback, []);
    const logout = useCallback<LogoutFn>(logoutCallback, []);
    const register = useCallback<RegisterFn>(registerCallback, []);
    const value = {isAuthenticated, username, login, logout, loginError, register ,registerError, isRegistered};
    useEffect(() => {
        const loadStoredCredentials = async () => {
            const storedUsername = await AsyncStorage.getItem('username');
            const storedPassword = await AsyncStorage.getItem('password');
            if (storedUsername && storedPassword) {
                await loginCallback(storedUsername, storedPassword, true); // Auto-login if credentials are stored
            }
        };
        loadStoredCredentials();
    }, []);

    async function loginCallback(loggingUsername?: string, password?: string, autoLogin = false) {
        log('login');
        try{
            log('authenticate...');
            //setUsername(loggingUsername);
            await loginApi(loggingUsername,password);
            setState(prevState => ({
                ...prevState,
                isAuthenticated: true,
                loginError: 0,
                registerError:0,
                username: loggingUsername,
                password,

              }));
            log('authenticate succeeded');
            if (!autoLogin) {
                // Save credentials if not auto-login
                await AsyncStorage.setItem('username', loggingUsername);
                await AsyncStorage.setItem('password', password);
            }

        }catch(error){
            log('authenticate failed');
            setState(prevState => ({
                ...prevState,
                isAuthenticated: false,
                loginError: prevState.loginError +1,
              }));
        }
    }
    async function logoutCallback() {
        log('logout');
        setState({
          ...initialState,
          isAuthenticated: false,
          loginError:0,
        });
        await AsyncStorage.removeItem('username');
        await AsyncStorage.removeItem('password');
      }
    async function registerCallback(loggingUsername?: string, password?: string) {
        log('register');
        try{
            setState({
                ...initialState,
                isRegistered: false,});
            await registerApi(loggingUsername,password);
            setState({
                ...initialState,
                isAuthenticated: false,
                loginError:0,
                registerError:0,
                isRegistered:true,
              });
              log('register succesful');
        }catch(error){
            log('register failed');
            setState(prevState => ({
                ...prevState,
                isAuthenticated: false,
                registerError: prevState.loginError +1,
                isRegistered: false,
              }));
        }
      }
    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}