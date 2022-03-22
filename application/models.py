from .database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# User Model
class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    hashed_password = db.Column(db.String, nullable=False)

    # Creating One-to-Many Relationship
    trackers = db.relationship("Tracker", backref='owner')
    logs = db.relationship("Log", backref='owner')

    @property
    def password(self):
        raise AttributeError("Password isn't a readable attribute!")

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return '<User Name %r , User_name  %r>' % (self.firstname, self.user_name)


# todo add Last tracked
class Tracker(db.Model):
    __tablename__ = "tracker"
    tracker_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tracker_name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(150))
    tracker_type = db.Column(db.String(150), nullable=False)
    settings = db.Column(db.String(150))
    last_reviewed = db.Column(db.DateTime(80))

    log = db.relationship('Log')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return '<Name %r>' % self.tracker_name



class Log(db.Model):
    # todo change timestamp from string to datetime
    __tablename__ = "log"
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    value = db.Column(db.Float)
    value_mcq_choice = db.Column(db.String(150))
    notes = db.Column(db.String(150))
    tracker_id = db.Column(db.Integer, db.ForeignKey('tracker.tracker_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return '<Log Name: %r log_date: %d>' % (self.tracker_name, self.added_date_time)
