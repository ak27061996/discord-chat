import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# User model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    # User contructor
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def json(self):
        return {
            "id": self.id,
            "username": self.username
        }, 200

    # Method to save user to DB
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user from DB by username
    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # Class method which finds user from DB by id
    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()



class Chat(db.Model):
    __tablename__ = "chats"
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    msg = db.Column(db.String(500))

    # User contructor
    def __init__(self, user_id, msg):
        self.user_id = user_id
        self.msg = msg
        self.chat_id = user_id   # when user chats with system

    def json(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "created_date": self.created_at,
            "user_id": self.user_id,
            "msg": self.msg
        }, 200

    # Method to save chat
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove chat from DB
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user's chat from DB by user_id and chat_id
    @classmethod
    def find_user_id_chats(cls, user_id, chat_id):
        return cls.query.filter_by(user_id=user_id, chat_id = chat_id)
    
    def find_google_chats_history(self):
        '''
          return chat history which start with '!google'
        '''
        return db.session.query(self).filter(self.msg.ilike('!google %')).all()[:3]

    def recent_search(self, query):
        '''
         find msg which contains some specific word
        '''
        return db.session.query(self).filter(self.msg.ilike('!google % {0} %'.format(query))).all()



