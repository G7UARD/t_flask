
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager #UserMixin, login_user, current_user, logout_user, login_required
from flask_mail import Mail
from flask_migrate import Migrate

app=Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/timur/OneDrive/Рабочий стол/T_flask/database/mydatabase.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tpostgres:tflask@localhost:5432/tflaskapp'
app.config['SECRET_KEY'] = 'your_seecret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ace173720@gmail.com'
app.config['MAIL_PASSWORD'] = 'temppasswordpython*123'
migrate = Migrate(app, db)
mail = Mail(app)
app.app_context().push()


from t_flask import routes

