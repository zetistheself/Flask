from flask_restful import reqparse, abort, Api, Resource
from . import db_session
from .users import User
from flask import jsonify



def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_user_not_found(users_id)
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        return jsonify({'user': user.to_dict(
            only=('email', 'user_id'))})

    def delete(self, users_id):
        abort_if_user_not_found(users_id)
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('email', required=True, type=str)
parser.add_argument('hashed_password', required=True, type=str)


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('email')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            email=args['email'],
            hashed_password=args['hashed_password'],
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})
