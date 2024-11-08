import React, { useCallback, useEffect, useState } from 'react';
import { View, Text, Button, SafeAreaView,StyleSheet, TextInput} from 'react-native';
import Checkbox from 'expo-checkbox';
import TimePicker from '../../components/UI/Pickers/TimePicker';
import { TaskProps } from './TaskProps';
import { useTasks } from './TaskProvider';
import { getLogger } from '../../core';

const log = getLogger('TaskEdit');

const EditTask = ({route, navigation}) => {
    const {activityId, handleSaveParam, date} = route.params || {};
    const {tasks} = useTasks();
    const [label, setLabel] = useState('');
    const [selectedStartTime, setSelectedStartTime] = useState(new Date(0,0,0,0,0));
    const [selectedDuration, setSelectedDuration] =  useState(new Date(0,0,0,0,0));
    const [selectedEndTime, setSelectedEndTime] =  useState(new Date(0,0,0,0,0));
    const [task, setTask] = useState<TaskProps>();
    const [isPreciseTime, setIsPreciseTime] = useState(false);

    useEffect(() =>{
      log('useEffect');
      const task = tasks?.find(t => t._id === activityId);
      setTask(task);
      if(task){
        setLabel(task.label);
        setIsPreciseTime(true);
        setSelectedStartTime(task.start_time ? new Date(0,0,0,task.start_time/60,task.start_time %60) : new Date(0,0,0,0,0));
        setSelectedEndTime(task.end_time ? new Date(0,0,0,Math.floor(task.end_time/60),task.end_time %60): new Date(0,0,0,0,0));
        setSelectedDuration(task.duration ? new Date(0,0,0,Math.floor(task.duration/60),task.duration %60): new Date(0,0,0,0,0));
      }
    },[activityId, tasks]);

    useEffect(() => {
      const endTime = new Date();
      endTime.setHours(selectedStartTime.getHours() + selectedDuration.getHours());
      endTime.setMinutes(selectedStartTime.getMinutes() + selectedDuration.getMinutes());
      setSelectedEndTime(endTime);
    },[selectedDuration, selectedStartTime]);

    const handleSave = useCallback(() => {
      const duration = format_time(selectedDuration);
      const start_time = format_time(selectedStartTime);
      const end_time = format_time(selectedEndTime);
      const editedTask = task ? {...task,label, start_time, end_time, duration,date}:{label, start_time, end_time, duration,date};
      if (typeof handleSaveParam === 'function') {
        handleSaveParam(editedTask);
        if (navigation.canGoBack()) {
          navigation.goBack();
        } else {
          console.log("Can't go back");
        }
        setSelectedStartTime(new Date());
        setSelectedEndTime(new Date());
        setSelectedDuration(new Date(0,0,0,0,0));
      }else {
        console.error('handleSaveParam is not a function or is undefined');
      }
    },[task, handleSaveParam,label, selectedStartTime, selectedEndTime, selectedDuration,date, navigation ]);

    const format_time = (time) => {
      return time.getHours() * 60 + time.getMinutes();
    }
    return (
        <SafeAreaView style={styles.centeredView}>
          <View >
            <View style={styles.modalView}>
              <View style={styles.timeContainer}>
              <Text style={styles.timeText}>Label:</Text>
                <TextInput
                  style={styles.input}
                  onChangeText={setLabel}
                  value={label}
                  placeholder="Enter task"
                  keyboardType="default"
                />
              </View>
              <View style={styles.checkboxContainer}>
                <Checkbox
                  value={isPreciseTime}
                  onValueChange={setIsPreciseTime}
                  style={styles.checkbox}
                />
                <Text style={styles.label}>Precise time</Text>
              </View>
              {isPreciseTime && (
                <>
                <TimePicker text={'Duration'} onConfirm={(time) => setSelectedDuration(time)} time_param={selectedDuration} />
                <TimePicker text={'Start time'} onConfirm={(time) => setSelectedStartTime(time)} time_param = {selectedStartTime}/>
                <TimePicker text={'End time'} onConfirm={(time) => setSelectedEndTime(time)} time_param = {selectedEndTime}/>
                </>
              )}
              <Button title="Add Task" onPress={handleSave} />
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
    width: 130,
    borderRadius: 5,
  },
  timeText: {
    fontSize: 18,
    marginVertical: 10,
  },
  timeContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: "space-between",
    marginVertical: 5,
    width:200,
  },
  button:{
    borderRadius: 5,
    backgroundColor: '#86B6F6',
  },
  checkboxContainer: {
    flexDirection: 'row',
    marginBottom: 20,
    alignItems: 'center',
    width:200,
  },
  checkbox: {
    alignSelf: 'center',
    height: 25,
    width: 25,
  },
  label: {
    margin: 8,
  },
});

export default EditTask;