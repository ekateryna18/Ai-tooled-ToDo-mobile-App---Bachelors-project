import React from 'react';
import { View, TouchableOpacity,Text, StyleSheet, SafeAreaView,  } from 'react-native';

const Toolbar = ({ handleAddButton, handleLogout, handleAI}) =>{
  return (
    <View style={styles.toolbar}>
      <TouchableOpacity style={styles.icon_container} onPress = {()=>handleLogout()}>
        {/* <SimpleLineIcons name="logout" size={35} color="#3c8dfa" /> */}
        <Text style={styles.text}>Logout</Text>
      </TouchableOpacity>
      <SafeAreaView >
        {/* <TouchableOpacity style={styles.addButton} onPress={() => setModalVisible(true)}> */}
        <TouchableOpacity style={styles.addButton} onPress={() => handleAddButton()}>
          <Text style={styles.plusText}>+</Text>
        </TouchableOpacity>
      </SafeAreaView>
      <View style={styles.icon_container}>
        <TouchableOpacity onPress={() => handleAI()}>
            <Text style={styles.text}>Use AI</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
    toolbar: {
      height: '10%',
      backgroundColor: '#EEF5FF',
      //justifyContent: 'center',
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
      color: '#3c8dfa',
      fontWeight: '500',
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
    addButton: {
      width: 70,
      height: 70,
      borderRadius: 40,
      backgroundColor: '#3c8dfa',
      //marginBottom: 30,
    //   backgroundColor: '#86B6F6',
      justifyContent: 'center',
      alignItems: 'center',
      shadowOpacity: 0.6,
      shadowRadius: 3,
      shadowColor: '#060625',
      shadowOffset: { width: 0, height: 2 },
      elevation: 5,
    },
    plusText: {
      color: 'white',
      fontSize: 30,
      fontWeight: 'bold',
    }
  });
export default Toolbar;