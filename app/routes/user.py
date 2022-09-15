from flask import Flask, request, jsonify
from flask_restx import Namespace, Resource, fields

from database import db
from .akun import get_password_hash, is_exist_user

api = Namespace('user', description='user crud')

# routes
get_user_parser = api.parser()
get_user_parser.add_argument('username', type=str, location='args', help='empty query to get all users')
@api.route('/')
@api.expect(get_user_parser)
class User_Get_All(Resource):
    def get(self):
        try: 
            collection = db['user']
            args = get_user_parser.parse_args()
            if args['username']:
                return jsonify(list( collection.find({ "username": args['username'] }, {"_id": 0}) )[0])
            else:
                return jsonify(list( collection.find({}, {"_id": 0}) ))
        except Exception as e:
            return { "message": "get data failed",
                     "detail": str(e) }

@api.route('/insert/<string:username>/<string:password>')
class User_Insert(Resource):
    def post(self, username, password):
        try:
            collection = db['user']
            collection.insert_one( {"username":username, "password": get_password_hash(password)} )
            return { "message": "insert data succesful" }
        except Exception as e:
            return { "message": "insert data failed",
                     "detail": str(e) }

update_user_parser = api.parser()
update_user_parser.add_argument('username', location='json')
update_user_parser.add_argument('password', location='json')
@api.route('/update/<string:username>')
@api.expect(update_user_parser)
class User_Update(Resource):
    def put(self, username):
        try:
            if not is_exist_user(username): return { "message": "username not found"}

            collection = db['user']
            args = update_user_parser.parse_args()
            args = dict((k, v) for k, v in args.items() if v)

            if "password" in args: args['password'] = get_password_hash(args['password'])

            collection.update_one({"username": username}, {"$set": args}, upsert=True)

            return { "message": "update data succesful"}
        except Exception as e:
            return { "message": "update data failed",
                     "detail": str(e) }

@api.route('/delete/<string:username>')
class User_Delete(Resource):
    def delete(self, username):
        try:
            if not is_exist_user(username): return { "message": "username not found"}

            collection = db['user']
            collection.delete_one({"username": username })

            return { "message": "delete data succesful"}
        except Exception as e:
            return { "message": "delete data failed",
                     "detail": str(e) }
