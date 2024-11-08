import { getLogger } from "../../core";
import { getTasksbyUsername, getTasksbyAlgorithm} from "./TaskApi";

const log = getLogger('useTasks');

export const fetchTasks = async (username) => {
    try{
        const tasks = await getTasksbyUsername(username);
        log('fetchTasks succeeded');
        return tasks;
    }catch(error){
        log('fetchTasks failed');
    }
}