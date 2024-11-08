import React, { useEffect, useState } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Platform } from 'react-native';
import { format, addDays, subDays } from 'date-fns';
import DateTimePickerModal from '@react-native-community/datetimepicker';

const DatePicker = ({onDateChanged, date}) => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [isDatePickerVisible, setDatePickerVisibility] = useState(false);
  useEffect(() => {
    if(date)
    { setSelectedDate(date);
    }
  },[date]);
  const handleChange = (event,date) => {
    const currentDate = date || selectedDate;
    setSelectedDate(currentDate);
    onDateChanged(currentDate);
    setDatePickerVisibility(Platform.OS === 'ios');
    hideDatePicker();
  };

  const showDatePicker = () => {
    setDatePickerVisibility(true);
  };

  const hideDatePicker = () => {
    setDatePickerVisibility(false);
  };
  const handleMinusArrow = (event,date) =>{
    const currentDate = subDays(selectedDate, 1);
    setSelectedDate(currentDate);
    onDateChanged(currentDate);
  }

  const handlePlusArrow = (event,date) =>{
    const currentDate = addDays(selectedDate, 1);
    setSelectedDate(currentDate);
    onDateChanged(currentDate);
  }
  return (
    <View style={styles.toolbar}>
      <TouchableOpacity onPress={handleMinusArrow}>
        <Text style={styles.arrow}>{"<"}</Text>
      </TouchableOpacity>
      <View style={styles.datePicker}>
      <DateTimePickerModal
        display="default"
        isVisible={isDatePickerVisible}
        mode="date"
        onChange={handleChange}
        value={selectedDate}
      />
      </View>
      {/* <TouchableOpacity onPress={showDatePicker}>
        <Text style={styles.dateText}>
          {format(selectedDate, 'EEE, MMMM dd')}
        </Text>
      </TouchableOpacity> */}
      <TouchableOpacity onPress={handlePlusArrow}>
        <Text style={styles.arrow}>{">"}</Text>
      </TouchableOpacity>
    </View>
  );
};

const styles = StyleSheet.create({
  toolbar: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 10,
    borderRadius: 5,
    width: '100%',
    alignSelf: 'center',
  },
  arrow: {
    color: '#3c8dfa',
    fontSize: 30,
  },
  datePicker: {
    // flex:1,
    display: 'flex',
    borderRadius: 5,
    backgroundColor: '#3c8dfa',
    justifyContent: 'center',
    alignItems: 'center',
    paddingRight:10,
    // paddingBottom:2,
    // paddingTop:2,
  }
});

export default DatePicker;
