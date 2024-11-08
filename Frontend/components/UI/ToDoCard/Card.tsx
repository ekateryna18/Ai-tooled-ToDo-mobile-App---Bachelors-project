import React, { useEffect, useState } from 'react';
import Checkbox from 'expo-checkbox';
import { View, Text, StyleSheet } from 'react-native';

const Card = ({label, duration, start_time, end_time, completed, onUpdate, showCheckBox }) =>{
  const [isChecked, setChecked] = useState(completed);
  const [showChB, setShowChB] = useState(showCheckBox);
  useEffect(() => {
    setShowChB(showCheckBox);
  },[showCheckBox]);

  const handleCheck = (check) => {
    setChecked(check);
    onUpdate(check);
  }
  return (
    <View style={[styles.card, completed ?  styles.cardIncomplete : styles.cardCompleted]} >
      <View style= {{flexDirection: 'row'}}>
      {showCheckBox && (
      <>
           <Checkbox style={styles.checkbox} value={isChecked} onValueChange={handleCheck} />
      </>
      )}

        <View>
        <Text style={styles.label}>{label}</Text>
        {
          (duration != '00:00') ?
          <>
           <Text>Duration: {duration}</Text>
          </>
          :
          <>
          <Text>Time not precised</Text>
          </>
        }
        </View>

      </View>
      { duration != '00:00' &&
      <>
      <View style = {{alignItems: 'center'}}>
        <Text style={styles.time_style}>{start_time}</Text>
        <Text style={styles.time_style}>|</Text>
        <Text style={styles.time_style}>{end_time}</Text>
      </View>
      </>
    }
    </View>
);}

const styles = StyleSheet.create({
  card: {
    //backgroundColor: '#EEF5FF',
    flexDirection: 'row',
    justifyContent: "space-between",
    padding: 20,
    marginVertical: 10,
    marginHorizontal: 20,
    borderRadius: 8,
    shadowOpacity: 0.4,
    shadowRadius: 3,
    shadowColor: '#060625',
    shadowOffset: { width: 0, height: 2 },
    elevation: 5,
    alignItems: 'center',
  },
  cardCompleted:{
    backgroundColor: 'white',
  },
  cardIncomplete:{
    backgroundColor: 'rgba(220, 220, 220, 0.5)',
  },
  label: {
    fontSize: 18,
    marginBottom: 5,
    fontWeight: 'bold',
  },
  checkbox: {
    margin: 10,
    height: 25,
    width: 25,
  },
  time_style:{
    fontSize: 15,
    marginBottom: 5,
    fontWeight: 'bold',
  },
});

export default Card;
