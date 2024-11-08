import configparser

from bson import ObjectId
from pymongo import MongoClient

from domain.Activity import Activity


class ActivityRepository:
    def __init__(self, database):
        self.__database__ = database
        self.__activities__ = self.__database__.users_schedule

    def add(self, activity, username):
        if activity.duration == 0:
            activity.start_time = 0
            activity.end_time = 0
            fixed_by_user = False
        else:
            fixed_by_user = True
        #print(self.__client__.list_database_names())
        self.__activities__.insert_one({
            "username":username,
            "label": activity.label,
            #"location":activity.location,
            "start_time":activity.start_time,
            "end_time":activity.end_time,
            "duration":activity.duration,
            "date":activity.date,
            "completed":False,
            "fixed_by_user":fixed_by_user
        })

    def get_activities(self, username):
        cursor = list(self.__activities__.find({'username': username}))
        return cursor

    def get_actvities_by_date(self, selected_date, username):
        cursor = list(self.__activities__.find({'username': username, 'completed': False, 'date':selected_date}))
        activities_list = []
        for activity in cursor:
            db_activity = {"_id": str(activity['_id']), "label": activity['label'],
                           "start_time": activity['start_time'],
                           "end_time": activity['end_time'], "duration": activity['duration'], "date": activity['date'],
                           "completed": activity['completed'],
                           "fixed_by_user": activity['fixed_by_user']}
            activities_list.append(db_activity)
        return activities_list
    def update(self, activity):
        self.__activities__.update_one({'_id': ObjectId(activity.id)},{"$set":{
            "label": activity.label,
            #"location":activity.location,
            "start_time":activity.start_time,
            "end_time":activity.end_time,
            "duration":activity.duration,
            "date":activity.date,
            "completed": activity.completed,
        }
           })

    def delete(self, id):
        self.__activities__.delete_one({"_id": ObjectId(id)})

    def add_dataset(self, lifeTRacking_dataset, username):
        # lifeTRacking_dataset = lifeTRacking_dataset.reset_index()
        # for index, row in lifeTRacking_dataset.iterrows():
        list_dict = [{"_id": '1', "username": "ecaterinamt","label": "prep","start_time": 320,"end_time": 335,"duration": 15,"date": "2019-05-01"},
                    {"_id":'2',"username": "ecaterinamt","label": "math","start_time": 335,"end_time": 395,"duration": 60,"date": "2019-05-01"},
                    {"_id": '2', "username": "ecaterinamt", "label": "prep", "start_time": 335, "end_time": 395,"duration": 60, "date": "2019-05-02"},
                    {"_id": '2', "username": "ecaterinamt", "label": "uni", "start_time": 335, "end_time": 395,"duration": 60, "date": "2019-05-03"},
                    {"_id": '2', "username": "ecaterinamt", "label": "cook", "start_time": 335, "end_time": 395,"duration": 60, "date": "2019-05-04"}]
        for row in  list_dict:
            self.__activities__.insert_one({
                "username":username,
                "label": row['label'],
                # "location":activity.location,
                "start_time": row['start_time'],
                "end_time": row['start_time'] + row['duration'],
                "duration": row['duration'],
                "date": row['date']
            })
        return True