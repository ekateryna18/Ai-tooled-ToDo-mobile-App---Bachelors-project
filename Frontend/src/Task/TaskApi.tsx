import { withLogs, baseUrl } from "../../core";
import { TaskProps } from "./TaskProps";
import axios from 'axios';

const taskUrl = `http://${baseUrl}/tasks`;

export const getTasks:() => Promise<TaskProps[]> = () => {
    return withLogs(axios.get(`${taskUrl}`), 'getTasks');
}
// export const getIncompleteTasksbyUsername: (username: string) => Promise<TaskProps[]> = (username) => {
//     return withLogs(axios.get(`${taskUrl}/incomplete/${username}`), 'getIncompleteTasksByUsername');
// }
// export const getCompleteTasksbyUsername: (username: string) => Promise<TaskProps[]> = (username) => {
//     return withLogs(axios.get(`${taskUrl}/complete/${username}`), 'getCompleteTasksByUsername');
// }
export const getTasksbyUsername: (username: string) => Promise<TaskProps[]> = (username) => {
    return withLogs(axios.get(`${taskUrl}/${username}`), 'getTasksByUsername');
}
export const getTasksbyAlgorithm: (username: string, selected_date: string) => Promise<TaskProps[]> = (username,selected_date) => {
    console.log(selected_date);
    return withLogs(axios.post(`http://${baseUrl}/usealgorithm/${username}`,{'selected_date':selected_date}), 'getTasksByAlgorithm');
}
export const addSchedule: (username: string) => Promise<TaskProps[]> = (username) => {
    return withLogs(axios.post(`http://${baseUrl}/schedule/${username}`),'keepSchedule');
}
export const createTask: (username:string, task: TaskProps) => Promise<TaskProps[]> = (username, task) => {
    return withLogs(axios.post(`${taskUrl}/${username}`,task), 'createTask');
}
export const updateTask: (username:string, task: TaskProps) => Promise<TaskProps[]> = (username, task) => {
    return withLogs(axios.put(`${taskUrl}/${username}/${task._id}`,task), 'updateTask');
}
export const deleteTask: (taskId : string)=> Promise<TaskProps[]> = (taskId) => {
    return withLogs(axios.delete(`${taskUrl}/${taskId}`),'deleteTask');
}
