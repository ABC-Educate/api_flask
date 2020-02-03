from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_claims
)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {
        'hello': identity,
        'foo': ['bar', 'baz']
    }


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {'access_token': create_access_token(username) ,
            'pinsheloco':'jaja'}
    return jsonify(ret), 200


# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    claims = get_jwt_claims()
    return jsonify({
        'hello_is': claims['hello'],
        'foo_is': claims['foo']
    }), 200


if __name__ == '__main__':
    app.run()