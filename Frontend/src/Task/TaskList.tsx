import { SafeAreaView,View, FlatList, StyleSheet,Animated,Text, Dimensions, LogBox  } from 'react-native';
import DatePicker from '../../components/UI/Pickers/DatePicker';
import Toolbar from '../../components/UI/Toolbar/Toolbar';
import Task from './Task';
import { useEffect, useState } from 'react';
import { useTasks } from './TaskProvider';
import { useLogin } from '../Login/AuthProvider';
import {Swipeable, TouchableOpacity} from 'react-native-gesture-handler';
import ToolbarAI from '../../components/UI/Toolbar/ToolbarAI';

const TaskList = ({navigation}) =>{
    LogBox.ignoreLogs([
        'Non-serializable values were found in the navigation state',
      ]);
    const [selectedDate, setSelectedDate] = useState(new Date());
    const {tasks, saveTask, deleteTask, loadTasksAlg, reloadTasks, keepSchedule} = useTasks();
    const { logout } = useLogin();
    const [showToolbars, setShowToolbars] = useState(true);


    const renderItem = ({ item }) => (
        <Swipeable renderRightActions={(progress,dragX) => renderRightActions(progress,dragX,item._id)}>
            <Task _id={item._id} onEdit={handleEditTask} onSave={(check) =>handleCheck(check,item)} label={item.label} start_time={item.start_time} end_time={item.end_time} duration={item.duration} completed={item.completed} showCheckBox={showToolbars}/>
        </Swipeable>
    );
    const renderRightActions = (progress,dragX, itemId) => {
        const opacity = dragX.interpolate({
          inputRange: [-150, 0],
          outputRange: [1, 0],
          extrapolate: 'clamp',
        });
        return (
          <View style={styles.swipedRow}>
            <View style={styles.swipedConfirmationContainer}>
              <Text style={styles.deleteConfirmationText}>Are you sure? {'\n'}To undo, swipe -{'>'}</Text>
            </View>
            <TouchableOpacity style={styles.deleteButton} onPress={() => handleDelete(itemId)}>
            {/* <TouchableOpacity style={[styles.deleteButton, {opacity}]} onPress={() => handleDelete(itemId)}> */}

                <Animated.View style={{opacity}}>
                    <Text style={styles.deleteButtonText}>Delete</Text>
                </Animated.View>
            </TouchableOpacity>
          </View>
        );
      };
    const handleLogout = () =>
    {
        console.log("logging out");
        logout();
        navigation.navigate('LoginMain');
    };
    const handleSave = (task) => {
        console.log("Task to add: ", task);
        saveTask(task);
    };
    const handleDelete = (itemId) => {
        console.log("task to delete "+ itemId);
        deleteTask(itemId);
    }
    const handleCheck = (check, task) => {
        task.completed = check;
        console.log("Task to add: ", task);
        saveTask(task);
    }

    const handleDateChanged = (date) =>{
        setSelectedDate(date);
    }
    const handleAddTask = () =>{
        navigation.navigate('EditTask', {
            activityId: null,
            handleSaveParam: handleSave,
            date: formatDate(selectedDate),
        });
        console.log("Navigate to add page ");
    }
    const handleEditTask = (id) => {
        navigation.navigate('EditTask', {
            activityId: id,
            handleSaveParam: handleSave,
            date: formatDate(selectedDate),
        });
        console.log("Navigate to edit page ");
    };

    const formatDate = (date) => {
        const year = date.getFullYear();
        const month = date.getMonth() + 1;
        const day = date.getDate();
        const formattedMonth = month < 10 ? `0${month}` : month;
        const formattedDay = day < 10 ? `0${day}` : day;
        const formattedDate = `${year}-${formattedMonth}-${formattedDay}`;
        return formattedDate;
      };
    const handleUseAi = () =>{
        setShowToolbars(false);

        const string_date = formatDate(selectedDate);
        console.log("load tasks by alg for " + string_date);
        loadTasksAlg(string_date);
    }
    const handleCancelAI = () => {
        setShowToolbars(true);
        reloadTasks();
    };
    const handleRetryAI = () => {
        handleUseAi();
    };
    const handleKeepSchedule = () => {
        keepSchedule();
        handleCancelAI();
    };
    return (
        <View style={styles.container}>
            <View style={styles.toptoolbar}>
                <SafeAreaView >
                {showToolbars && (
                <>
                    <DatePicker onDateChanged={handleDateChanged} date={selectedDate}/>
                </>
                )}
                {!showToolbars && (
                <>
                    <Text style = {styles.toptext}>Generated list for: {selectedDate.getDate()}-{selectedDate.getMonth()+1}-{selectedDate.getFullYear()}</Text>
                </>
                )}
                </SafeAreaView>
            </View>

            <FlatList
                data={tasks
                    .filter(task =>
                        task.date == formatDate(selectedDate))
                    .sort((a,b) => a.start_time - b.start_time)
                    }
                // data={filteredAndSortedTasks}
                renderItem={renderItem}
                keyExtractor={(item) => { return item._id}}
            />
            {showToolbars && (
            <>
            <Toolbar handleAddButton={handleAddTask} handleLogout={handleLogout} handleAI={handleUseAi}/>
            </>
            )}
            {!showToolbars && (
            <>
            <ToolbarAI handleCancel={handleCancelAI} handleKeep={handleKeepSchedule} handleRetry={handleRetryAI}/>
            </>
            )}
        </View>
      );
}
const styles = StyleSheet.create({
    container: {
        flex: 1,
        ///marginTop: 50,
        backgroundColor: '#86B6F6',
      },
    toptoolbar:{
      alignItems: 'center',
      backgroundColor: '#EEF5FF',
      shadowOpacity: 0.6,
      shadowRadius: 3,
      shadowColor: '#060625',
      shadowOffset: { width: 0, height: 2 },
      elevation: 5,
    },
    swipedRow: {
        flexDirection: 'row',
        flex: 1,
        alignItems: 'center',
        paddingLeft: 5,
        backgroundColor: '#3c8dfa',
        margin: 20,
        minHeight: 50,
        borderRadius:8,
        justifyContent: 'center',
        shadowOpacity: 0.6,
        shadowRadius: 3,
        shadowColor: '#060625',
        shadowOffset: { width: 0, height: 2 },
        elevation: 5,
    },
    swipedConfirmationContainer: {
        flex: 1,
     },
    deleteConfirmationText: {
        color: '#fcfcfc',
        fontWeight: 'bold',
        margin:20,
    },
    deleteButton: {
        backgroundColor: '#b60000',
        flexDirection: 'column',
        justifyContent: 'center',
        height: '60%',
        width: 70,
        borderRadius:8,
        alignItems: 'center',
        margin:20,
    },
    deleteButtonText: {
        color: '#fcfcfc',
        fontWeight: 'bold',
    },
    toptext:{
        fontSize: 18,
        marginTop: 10,
        marginBottom: 10,
    },
});

export default TaskList;