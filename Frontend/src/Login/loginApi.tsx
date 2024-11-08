import { withLogs, baseUrl } from "../../core";
import axios from 'axios';

const loginUrl = `http://${baseUrl}/login`;
const registerUrl = `http://${baseUrl}/register`;

export interface AuthProps{
    username: string;
}

export const login: (username?:string, password?:string) => Promise<AuthProps> = (username, password) => {
    return withLogs(axios.post(loginUrl, { username, password }), 'login');
}
export const register: (username?:string, password?:string) => Promise<AuthProps> = (username, password) => {
    return withLogs(axios.post(registerUrl, { username, password }), 'register');
}