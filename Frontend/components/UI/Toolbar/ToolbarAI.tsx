import React from 'react';
import { View, TouchableOpacity,Text, StyleSheet, SafeAreaView,  } from 'react-native';

const ToolbarAI = ({ handleCancel, handleRetry, handleKeep}) =>{
  return (
    <View style={styles.toolbar}>
        <View style={styles.icon_container}>
            <TouchableOpacity onPress = {()=>handleCancel()}>
                <Text style={[styles.text, styles.blue]}>Cancel</Text>
            </TouchableOpacity>
        </View>
        <View style={styles.icon_container}>
            <TouchableOpacity onPress={() => handleRetry()}>
                <Text style={[styles.text, styles.red]}>Retry</Text>
            </TouchableOpacity>
        </View>
        <View style={styles.icon_container}>
            <TouchableOpacity  onPress={() => handleKeep()}>
                <Text style={[styles.text,styles.green]}>Keep</Text>
            </TouchableOpacity>
        </View>
    </View>
  );
};

const styles = StyleSheet.create({
    toolbar: {
      height: '10%',
      backgroundColor: '#EEF5FF',
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between',
      alignItems: 'center',
      shadowOpacity: 0.6,
      shadowRadius: 3,
      shadowColor: '#060625',
      shadowOffset: { width: 0, height: 2 },
      elevation: 5,
    },
    text:{
      fontSize: 19,
      fontWeight: '500',
    },
    blue:{
        color: '#3c8dfa',
    },
    red:{
        color: '#fc6d6d',
    },
    green:{
        color: '#529c5f',
    },
    icon_container:{
      width: 90,
      alignItems: 'center',
      flexDirection: 'column',
      justifyContent: 'center',
      backgroundColor: 'white',
      borderRadius:10,
      margin:10,
      height:40,
      shadowOpacity: 0.3,
      shadowRadius: 2,
      shadowColor: '#060625',
      shadowOffset: { width: 0, height: 2 },
      elevation: 3,
    },
  });
export default ToolbarAI;