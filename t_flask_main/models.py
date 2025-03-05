from t_flask import db, login_manager, app
from datetime import datetime
import jwt
from time import time
from flask_login import UserMixin
from flask import redirect, url_for
from t_flask.utils import generate_token, verify_token


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.now())
    details = db.relationship('UserDetails', backref='parent', lazy=True)

    def get_token(self, expires_sec=600):
        return jwt.encode({'user_id': self.id, 'exp': time() + expires_sec},
                        app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f'{self.username} : {self.email} : {self.date_created.strftime("%d/%m/%Y, %H:%M:%S")}'

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname =db.Column(db.String(20), unique=True, nullable=False)
    lastname =db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.firstname} {self.lastname}'