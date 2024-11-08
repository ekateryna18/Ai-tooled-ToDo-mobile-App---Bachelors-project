import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { Task } from 'react-native';
import { TaskProps } from './TaskProps';
import { fetchTasks } from './useTasks';
import { getLogger } from '../../core';
import { createTask, deleteTask as deleteTaskApi, getTasksbyAlgorithm, updateTask,addSchedule } from './TaskApi';
import { useLogin } from '../Login/AuthProvider';

const log = getLogger('TaskProvider');
type SaveTaskFn = (movie : TaskProps) => Promise<any>;
type DeleteTaskFn = (taskId: string) => Promise<any>;
type LoadTasksFn = (selectedDate: string) => Promise<any>;
type ReloadTasks = () => Promise<any>;
type KeepSchedule = () => Promise<any>;

export interface TaskState{
    tasks? : TaskProps[],
    saveTask? : SaveTaskFn,
    deleteTask?: DeleteTaskFn,
    loadTasksAlg?: LoadTasksFn,
    reloadTasks?: ReloadTasks,
    keepSchedule?: KeepSchedule,
}
const initialState: TaskState = {};

const TaskContext = createContext<TaskState>(initialState);

export const useTasks = () => useContext(TaskContext);

export const TaskProvider = ({children}) => {
    const [tasks, setTasks] = useState([]);
    const {isAuthenticated, username, login } = useLogin();
    const [isChanged, setIsChanged] = useState(0);
    const saveTask = useCallback<SaveTaskFn>(saveTaskCallback,[username]);
    const deleteTask = useCallback<DeleteTaskFn>(deleteTaskCallback,[]);
    const loadTasksAlg = useCallback<LoadTasksFn>(loadTasksbyAlgorithmCallback,[username]);
    const reloadTasks = useCallback<ReloadTasks>(loadTasks,[username]);
    const keepSchedule = useCallback<KeepSchedule>(keepScheduleCallback, [username]);
    const value = {tasks, saveTask, deleteTask, loadTasksAlg, reloadTasks, keepSchedule};
    useEffect( () => {
        console.log(isChanged);
        loadTasks();
    },[isChanged]);

    useEffect(() => {
        loadTasks();
    },[username]);

    async function loadTasks(){
        try{
            log(username);
            if(username != '')
            {
                const fetchedTasks = await fetchTasks(username);
                setTasks(fetchedTasks);
            }
        }catch (error) {
            console.error("Failed to load tasks:", error);
        }
    };

    async function loadTasksbyAlgorithmCallback(selectedDate: string){
        try{
            log("loadTasksbyAlgorithmCallback " + username + " " + selectedDate);
            if(username != '')
            {
                const fetchedTasks = await getTasksbyAlgorithm(username, selectedDate);
                setTasks(fetchedTasks);
            }
        }catch (error) {
            console.error("Failed to load tasks by algorithm:", error);
        }
    };
    async function keepScheduleCallback(){
        try{
            log("Keeping schedule");
            await addSchedule(username);
            //setIsChanged(prevIsChanged => prevIsChanged + 1);
        }catch(error){
            console.error("Error adding schedule: ", error);
        }
    }
    async function saveTaskCallback(task: TaskProps){
        try{
            log('saveTask started' + task);
            log("username " + username);
            const savedTask = await(task._id ? updateTask(username,task) : createTask(username,task));
            setIsChanged(prevIsChanged => prevIsChanged + 1);
            // console.log(isChanged);
            log('saveTask succeeded');
        }catch(error){
            console.error("Failed to save task: ", error);
        }
    };
    async function deleteTaskCallback(taskId: string){
        try{
            log("deleting task with id: "+ taskId);
            await deleteTaskApi(taskId);
            setIsChanged(prevIsChanged => prevIsChanged + 1);
            log('deleteTask succeeded');
        }catch(error){
            console.error("Failed to delete task: ", error);
        }
    }
    return (
        <TaskContext.Provider value={value}>
          {children}
        </TaskContext.Provider>
      );
}
