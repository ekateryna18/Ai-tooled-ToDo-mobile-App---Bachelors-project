import React, {useEffect, useState} from 'react';
import { format } from 'date-fns';
import DateTimePickerModal from 'react-native-modal-datetime-picker';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';

const TimePicker = ({text, onConfirm,  time_param}) => {
    const [isTimePickerVisible, setTimePickerVisibility] = useState(false);
    const [time, setTime] = useState(time_param);
    useEffect(() => {
      setTime(time_param);
    },[time_param]);
    const showTimePicker = () => {
      setTimePickerVisibility(true);
    };
    const hideTimePicker = () => {
        setTimePickerVisibility(false);
      };
    const handleConfirm = (timeConfirmed) => {
        setTime(timeConfirmed);
        onConfirm(timeConfirmed);
        hideTimePicker();
    }
    return(
        <View style={styles.timeContainer}>
            <Text style={styles.timeText}>{text}:</Text>
            <TouchableOpacity onPress={showTimePicker}>
                <View style={styles.timeTouchable}>
                    <Text style={styles.timeText}>
                        {format(time, 'HH:mm')}
                    </Text>
                </View>
            </TouchableOpacity>

              <DateTimePickerModal
                isVisible={isTimePickerVisible}
                mode="time"
                onConfirm={handleConfirm}
                onCancel={hideTimePicker}
                textColor='#000'
              />
        </View>
    );
}
const styles = StyleSheet.create({
    timeContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: "space-between",
        marginVertical: 5,
        width:200,
      },
    timeText: {
      fontSize: 18,
      marginVertical: 8,
    },
    timeTouchable: {
        backgroundColor: '#f0f0f0',  // Light grey background for visibility
        // padding: 5,
        borderRadius: 5,
        width: 70,
        marginLeft: 10,
        alignItems: 'center',
      },
  });
  export default TimePicker;