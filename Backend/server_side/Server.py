from flask import Flask, jsonify
from flask_cors import CORS
from flask import request, Response
class Server:
    def __init__(self, service):
        self.app = Flask(__name__)
        self.setup_config()
        self.setup_routes()
        CORS(self.app)
        self.__service__ = service
    def setup_config(self):
        self.app.config['DEBUG'] = True

    def setup_routes(self):
        # routes
        @self.app.route('/tasks')
        def activities():
            return [{"_id": '1', "username": "ecaterinamt","label": "prep","start_time": 320,"end_time": 335,"duration": 15,"date": "2019-05-01"},
                    {"_id":'2',"username": "ecaterinamt","label": "math","start_time": 335,"end_time": 395,"duration": 60,"date": "2019-05-01"},
                    {"_id": '2', "username": "ecaterinamt", "label": "prep", "start_time": 335, "end_time": 395,"duration": 60, "date": "2019-05-02"},
                    {"_id": '2', "username": "ecaterinamt", "label": "uni", "start_time": 335, "end_time": 395,"duration": 60, "date": "2019-05-03"},
                    {"_id": '2', "username": "ecaterinamt", "label": "cook", "start_time": 335, "end_time": 395,"duration": 60, "date": "2019-05-04"}]

        # @self.app.route('/tasks/incomplete/<string:username>', methods=['GET'])
        # def get_incomplete_activities(username):
        #     print(f"Fetching tasks for user: {username}")
        #     return self.__service__.get_activities(username,False)
        #
        # @self.app.route('/tasks/complete/<string:username>', methods=['GET'])
        # def get_complete_activities(username):
        #     print(f"Fetching tasks for user: {username}")
        #     return self.__service__.get_activities(username, True)

        @self.app.route('/tasks/<string:username>', methods=['GET'])
        def get_all_activities(username):
            print(f"Fetching tasks for user: {username}")
            return self.__service__.get_activities(username)

        @self.app.route('/tasks/<string:username>', methods = ['POST'])
        def add_activity(username):
            body_dict = request.json
            print(f"Adding activity to user: {username}")
            self.__service__.add_actvity(username,body_dict['label'], body_dict['start_time'], body_dict['end_time'], body_dict['duration'], body_dict['date'])
            print(body_dict)
            return body_dict

        @self.app.route('/tasks/<string:username>/<string:id>', methods=['PUT'])
        def update_activity(username,id):
            body_dict = request.json
            print(f"Updating activity to user: {username}")
            self.__service__.update_activity(id, body_dict['label'], body_dict['start_time'], body_dict['end_time'],
                                         body_dict['duration'], body_dict['date'], body_dict['completed'])
            print(body_dict)
            return body_dict

        @self.app.route('/tasks/<string:id>', methods = ['DELETE'])
        def delete_activity(id):
            boolean_result = self.__service__.delete_activity(id)
            if boolean_result is True:
                return Response( "Deletion successful",status=200, mimetype='application/json')
            else:
                return Response("Deletion failed", status=400, mimetype='application/json')
        @self.app.route('/schedule/<string:username>',methods=['POST'])
        def keep_schedule(username):
            boolean_result = self.__service__.keep_schedule()
            if boolean_result is True:
                return Response("Schedule added", status=200, mimetype='application/json')
            else:
                return Response("Error adding schedule", status=400, mimetype='application/json')

        @self.app.route('/login', methods = ['POST'])
        def login_user():
            body_dict = request.json
            boolean_result = self.__service__.login_user(body_dict['username'], body_dict['password'])
            print(f"Logging user: {body_dict['username']} Result: {boolean_result}")
            if boolean_result is True:
                return Response(body_dict['username'], status=200, mimetype='application/json')
            else:
                return Response("Password or username incorrect", status=400, mimetype='application/json')

        @self.app.route('/register', methods=['POST'])
        def register_user():
            body_dict = request.json
            boolean_result = self.__service__.register_user(body_dict['username'], body_dict['password'])
            print(f"Registering user: {body_dict['username']} Result: {boolean_result}")
            if boolean_result is True:
                return Response(body_dict['username'], status=200, mimetype='application/json')
            else:
                return Response("User already exists", status=400, mimetype='application/json')

        @self.app.route('/usealgorithm/<string:username>', methods=['POST'])
        def use_GA(username):
            body_dict = request.json
            selected_date = body_dict['selected_date']
            print(f"running algorithm for date {selected_date}")
            result = self.__service__.run_GA(selected_date,username)
            print(result)
            return result


    def run(self):
        self.app.run(host = '0.0.0.0', port = 5000)