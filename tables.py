from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db # must change when uploading

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    contributorID = db.Column(db.Integer, db.ForeignKey('users.id'))
    completed = db.Column(db.Boolean, default=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

class Update(db.Model):
    __tablename__ = 'updates'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400), nullable=False)
    contributorID = db.Column(db.Integer, db.ForeignKey('users.id'))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<UpdateID %r' % self.id

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable = False)
    passwordHash = db.Column(db.String(128), nullable=False)
    access = db.Column(db.Integer, nullable=False, default=1)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    confirmed = db.Column(db.Boolean, default=False)

    goals = db.relationship('Goal', backref='goals')
    updates = db.relationship('Update', backref='updates')

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.passwordHash = generate_password_hash(password)

    def verifyPassword(self, password):
        return check_password_hash(self.passwordHash, password)

    def generateToken(self, expiration=3600): # generates a confirmation token
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')
    
    def confirm(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id: # if the IDs don't match
            return False
        self.confirmed = True
        db.session.add(self)
        return True