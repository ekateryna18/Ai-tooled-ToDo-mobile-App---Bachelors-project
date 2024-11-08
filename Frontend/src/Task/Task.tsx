import { TouchableOpacity } from "react-native";
import Card from "../../components/UI/ToDoCard/Card";
import { TaskProps } from "./TaskProps";
import React from 'react';

interface TaskPropsExt extends TaskProps{
    onEdit: (_id?: string) => void;
    onSave: (check?:boolean) => void;
    showCheckBox: boolean;
}

const Task: React.FC<TaskPropsExt> = ({_id, label, duration, start_time, end_time,completed, onEdit, onSave, showCheckBox}) =>{
    const formatTime = (time) =>{
        var rest = time%60;
        let hour = (time - rest)/60;
        const minutes = time - hour*60;
        hour = ((time - rest)/60)%24;
        const formattedHour = hour < 10 ? `0${hour}` : hour;
        const formattedMinutes = minutes < 10 ? `0${minutes}` : minutes;
        return `${formattedHour}:${formattedMinutes}`;
    }
    const updateCheck = (check) => {
        completed = check;
        onSave(check);
        console.log(check);
    }
    return(
        <TouchableOpacity onPress = {() => onEdit(_id)} >
            <Card label={label} duration={formatTime(duration)} start_time={formatTime(start_time)} end_time={formatTime(end_time)} completed={completed} onUpdate={updateCheck} showCheckBox={showCheckBox}/>
        </TouchableOpacity>
    );
};

export default Task;