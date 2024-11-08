from datetime import datetime

from AI.data_processing import convert_date_to_weekday
from domain.Activity import Activity
import bcrypt

from domain.User import User


class Service:
    def __init__(self, activity_repository, user_repository, mainGA):
        self.__activity_repository__ = activity_repository
        self.__user_repository__ = user_repository
        self.__mainGA__ = mainGA
        #dictionary
        self.__last_schdeule__ = []

    def get_activities(self,username):
        activities_list = []
        cursor_list = self.__activity_repository__.get_activities(username)

        for activity in cursor_list:
            # db_activity = Activity(activity['label'], activity['start_time'], activity['end_time'],
            #                        activity['duration'], activity['date'])
            # db_activity.id = activity['_id']
            db_activity = {"_id": str(activity['_id']), "label":activity['label'], "start_time": activity['start_time'],
                           "end_time": activity['end_time'], "duration" : activity['duration'], "date" :  activity['date'], "completed":activity['completed'],
                           "fixed_by_user": activity['fixed_by_user']}
            activities_list.append(db_activity)
        return activities_list

    def add_actvity(self,username, label, start_time, end_time, duration, date):
        actvity = Activity(label,None, start_time,end_time,duration,date)
        print("Service - ")
        print(actvity)
        self.__activity_repository__.add(actvity,username)

    def login_user(self, username, password):
        user = self.__user_repository__.find_one_by_username(username)
        if user is not None and bcrypt.checkpw(password.encode('utf-8'), bytes(user['password'], encoding='utf8')):
            return True
        else:
            return False
    def register_user(self, username, password):
        user = self.__user_repository__.find_one_by_username(username)
        if user is None:
            user = User(username, password)
            self.__user_repository__.add(user)
            return True
        else:
            return False
    def update_activity(self,id, label, start_time, end_time, duration, date,completed):
        activity = Activity(label,None, start_time,end_time,duration,date)
        activity.id = id
        activity.completed = completed
        self.__activity_repository__.update(activity)

    def keep_schedule(self):
        try:
            for activity in self.__last_schdeule__:
                print(activity)
                self.update_activity(activity['_id'],activity['label'],activity['start_time'],activity['end_time'],activity['duration'],activity['date'],activity['completed'])
            return True
        except Exception as error:
            print(error)
            return False

    def delete_activity(self, id):
        try:
            self.__activity_repository__.delete(id)
            return True
        except:
            return False

    def run_GA(self,selected_date,username):
        current_time = datetime.now()
        time_minutes = current_time.hour * 60+ current_time.minute
        weekday = convert_date_to_weekday(selected_date)
        self.__last_schdeule__ = self.__activity_repository__.get_actvities_by_date(selected_date,username)
        # for activity in activities:
        #
        #     a = Activity(activity['label'], None, activity['start_time'], activity['end_time'], activity['duration'],  activity['date'])
        #     a.id = activity['_id']
        #     self.__last_schdeule__.append(a)

        correspondent_schedule = self.__mainGA__.main_GA(weekday,self.__last_schdeule__,time_minutes)
        for i in range(0,len(correspondent_schedule)):
            self.__last_schdeule__[i]['start_time'] = int(correspondent_schedule[i][0])
            self.__last_schdeule__[i]['duration'] = int(correspondent_schedule[i][1])
            self.__last_schdeule__[i]['end_time'] = int(correspondent_schedule[i][0] + correspondent_schedule[i][1])
        print(self.__last_schdeule__)
        return self.__last_schdeule__

