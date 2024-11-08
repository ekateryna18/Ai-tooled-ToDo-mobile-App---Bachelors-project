import configparser
from pymongo import MongoClient

from AI.GA.mainGAExp2 import MainGA
from domain.Activity import Activity
from repository.ActivityRepository import ActivityRepository
from repository.UserRepository import UserRepository
from server_side.Server import Server
from service.Service import Service


def init_database():
    config = configparser.ConfigParser()
    config.read('repository/config.ini')
    client = MongoClient(config.get('Database','connection_string'))
    database = client.daily_activities
    salt = config.get('Database', 'bcrypt_salt')
    return database, salt

def run():
    database, salt = init_database()
    activty_repo = ActivityRepository(database)
    users_repo = UserRepository(database, salt)
    mainGA = MainGA()
    service = Service(activty_repo, users_repo,mainGA)
    activities = test_activ()
    weekday = 3
    current_time = 420
    #mainGA.main_GA(weekday,activities,current_time)
    # user = User("tester", "tester")
    # users_repo. add(user)
    # service.login_user("nknik","tester")

    #service.run_GA("2024-07-01", "tester")
    # service.keep_schedule()
    server = Server(service)
    server.run()

def test_activ():
    a1 = Activity("uni")
    a2= Activity("math")
    a3 = Activity("sleep")
    a4 = Activity("prep")
    a5=Activity("cook")
    a8 = Activity("meditation")
    a9 = Activity("special")
    a10 = Activity("work")
    activities = [a1,a2,a3,a4,a5,a8,a9,a10]
    return activities

if __name__ == '__main__':
    run()
