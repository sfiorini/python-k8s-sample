from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

USERS = [
    {'email': 'john.doe@example.com',
     'firstName': 'John',
     'lastName': "Doe"},

    {'email': 'mary.jane@mydomain.com',
     'firstName': 'Mary',
     'lastName': "Jane"},
]


# Return current array index of user or abort if user does not exist.
def user_exist(user_email):
    index = next((i for i, item in enumerate(USERS)
                 if item['email'] == user_email), -1)
    if (index < 0):
        abort(404, message="User email {} doesn't exist".format(user_email))
    
    return index


parser = reqparse.RequestParser()
parser.add_argument('email', required=True, type=str,
                    help="Email is required")
parser.add_argument('firstName', required=True, type=str)
parser.add_argument('lastName', required=True, type=str)

# Parser for put does not need email argument.
parserPut = reqparse.RequestParser()
parserPut.add_argument('firstName', required=True, type=str)
parserPut.add_argument('lastName', required=True, type=str)

# User
# Get a single user, lets you modify or delete a user
class User(Resource):
    def get(self, user_email):
        index = user_exist(user_email)
        return USERS[index]

    def delete(self, user_email):
        index = user_exist(user_email)
        del USERS[index]
        return '', 204

    def put(self, user_email):
        args = parserPut.parse_args()
        index = user_exist(user_email)
        firstName = args['firstName']
        lastName = args['lastName']
        if (firstName): 
            USERS[index]['firstName'] = firstName
        if (lastName): 
            USERS[index]['lastName'] = firstName
        return USERS[index], 201


# Users
# List all users and add user (POST)
class Users(Resource):
    def get(self):
        return USERS

    def post(self):
        args = parser.parse_args()
        USERS.append(args)
        return USERS, 201


# Main
# Main route that simply display a message confirming the server is up and running
#
class Main(Resource):
    def get(self):
        return {'message': 'API Server is running successfully'}


##
# Api resource routing
##
api.add_resource(Main, "/")
api.add_resource(Users, '/user')
api.add_resource(User, '/user/<user_email>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
