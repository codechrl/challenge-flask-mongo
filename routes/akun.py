from flask_restx import Namespace, Resource, fields
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import datetime, timedelta
from jose import jwt

from database import db

# route
api = Namespace('akun', description='login & resgister')

# func
SECRET_KEY = "rahasia"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

def authenticate_user(username, password):
    if is_exist_user(username):
        collection = db['user']
        hashed_password = collection.find_one({ "username": username }, {"_id": 0})['password']
        if verify_password(password, hashed_password):
            return True
    else: return False

def is_exist_user(username):
    collection = db['user']
    if len(list( collection.find({ "username": username }, {"_id": 0}) )) == 0 :
        return False
    else:
        return True

def get_password_hash(password):
    return sha256.hash(password)

def verify_password(plain_password, hashed_password):
    return sha256.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# routes
@api.route('/login/<string:username>/<string:password>')
class Login(Resource):
    def post(self, username, password):
        try:
            collection = db['user']
            #return authenticate_user(username, password)
            if not authenticate_user(username, password):
                return { "message": "username or password is not correct" }
            else:
                access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = create_access_token( data={"username": username},
                                                    expires_delta=access_token_expires,
                                                    )
                return {
                        "access_token": access_token,
                        "token_type": "bearer",
                        "expired_in": str((datetime.utcnow() + access_token_expires).isoformat()),
                        "user_profile": {
                            "username": username,
                        },
                    }
        except Exception as e:
            return { "message": "login failed",
                     "detail": str(e) }       

@api.route('/register/<string:username>/<string:password>')
class Register(Resource):
    def post(self, username, password):
        try:
            collection = db['user']
            if is_exist_user(username):
                return { "message": "username already exist" }
            else:
                collection.insert_one( {"username":username, "password": get_password_hash(password)} )
                return { "message": "register succesful" }
        except Exception as e:
            return { "message": "register failed",
                     "detail": str(e) }