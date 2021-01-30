import os
from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user, login_required
from flask_mail import Mail

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
application = app
Bootstrap(app)
mail = Mail()
mail.init_app(app)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'projectData.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from auth import auth as authBlueprint
app.register_blueprint(authBlueprint, url_prefix='/auth')

loginManager = LoginManager()
loginManager.login_view = 'auth.login'
loginManager.init_app(app)

from manageProj import proj as projBlueprint
app.register_blueprint(projBlueprint, url_prefix='/proj')

PRIMARY_GOAL = "Win the Robotics Competition!"

@app.shell_context_processor
def make_shell_context():
    from tables import Goal, Update, User
    return dict(db=db, Goal=Goal, Update=Update, User=User)

@loginManager.user_loader
def loadUser(userID):
    from tables import User
    return User.query.get(int(userID))

@app.route('/', methods=['POST','GET'])
def index():
    from tables import User
    admins = User.query.filter(User.access >= 2)
    return render_template('index.html', admins=admins)


@app.route('/goals', methods=['GET','POST'])
@login_required
def goals():
    from tables import User
    if (current_user.access >= 2):
        leader = User.query.filter(User.access == 3).first()
        admins = User.query.filter(User.access == 2)
        members = User.query.filter(User.access == 1)
        return render_template('goals.html', leader=leader, admins=admins, members=members)
    else:
        flash("Error")
        return redirect(url_for('index'))
    
@app.route('/users', methods=['GET'])
@login_required
def users():
    from tables import User
    if (current_user.access >= 2):
        leader = User.query.filter(User.access == 3).first()
        admins = User.query.filter(User.access == 2)
        members = User.query.filter(User.access == 1)
        return render_template('users.html', leader=leader, admins=admins, members=members)
    else:
        flash("Cannot access the full list of users.")
        return redirect(url_for('index'))