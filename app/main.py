from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse

#  
from database import db
from routes import (
    akun,
    user
)

app = Flask(__name__)

# restx
api = Api(app,
        version='1.0',
        title='Prototype Project',
        description='A simple Prototype Project',
        doc='/api/docs'
)

# routes
api.add_namespace(akun.api)
api.add_namespace(user.api)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)