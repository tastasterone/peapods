from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    '''Users model'''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    
    @classmethod
    def signup(cls, username, password, first_name, last_name, email):
        '''Sign up new user'''

        hashed_password = bcrypt.generate_password_hash(password=password).decode('UTF-8')
        new_user = User(
            username=username,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        db.session.add(new_user)
        return new_user

    @classmethod
    def authenticate(cls, username,  password):
        '''Check user and password'''
        user = User.query.filter_by(username=username).first()
        password = bcrypt.check_password_hash(user.password, password)
        if user:
            if password:
                return user
        return False

class Pod(db.Model):
    '''Pods/teams model'''
    __tablename__ = 'pods'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.Text)

class SubPod(db.Model):
    __tablename__ = 'sub_pods'
    id = db.Column(db.Integer, db.ForeignKey('pods.id'), primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

class PodUser(db.Model):
    '''Users assigned to Pods'''
    __tablename__ = 'pod_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pod_id = db.Column(db.Integer, db.ForeignKey('pods.id', ondelete='cascade'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    owner = db.Column(db.Boolean, default=False)

class SubPodUser(db.Model):
    __tablename__ = 'sub_pod_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pod_id = db.Column(db.Integer, db.ForeignKey('pods.id', ondelete='cascade'))
    sub_pod_id = db.Column(db.Integer, db.ForeignKey('sub_pods.id', ondelete='cascade'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    owner = db.Column(db.Boolean, default=False)
    
class Message(db.Model):
    '''User messages'''
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class PodMessage(db.Model):
    '''User messages'''
    __tablename__ = 'pod_messages'
    pod_id = db.Column(db.Integer, db.ForeignKey('pods.id', ondelete='cascade'), primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'), primary_key=True)

class SubPodMessage(db.Model):
    '''User messages'''
    __tablename__ = 'sub_pod_messages'
    sub_pod_id = db.Column(db.Integer, db.ForeignKey('sub_pods.id', ondelete='cascade'), primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'), primary_key=True)
    
class Hobby(db.Model):
    '''User hobbies/activities/intrests'''
    __tablename__ = 'hobbies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=True, unique=True)
    description = db.Column(db.Text)

class UserHobby(db.Model):
    '''Hobbies to users'''
    __tablename__ = 'user_hobbies'
    hobby_id = db.Column(db.Integer, db.ForeignKey('hobbies.id', ondelete='cascade'), primary_key=True )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)