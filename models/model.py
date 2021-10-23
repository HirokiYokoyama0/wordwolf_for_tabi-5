from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy.sql import func
#from sqlalchemy.dialects import postgresql

app = Flask(__name__)

db = SQLAlchemy(app) ### for userdata
db2 = SQLAlchemy(app) ### for OtherVariable
db3 = SQLAlchemy(app) ### for worddata

class MemberList(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    comment = db.Column(db.String(128), nullable=False)
    vote_num = db.Column(db.Integer, nullable=False)
    ulf_flg = db.Column(db.Integer, nullable=False)
    to_vote = db.Column(db.Integer, nullable=False)
    to_vote2 = db.Column(db.Integer, nullable=False)
    prepare_flg = db.Column(db.Integer, nullable=False)

    def __init__(self, username=None, comment=None, vote_num = 0 , ulf_flg = 0 ,to_vote = 0,to_vote2 = 0,prepare_flg = 0
    ):
        self.username = username
        self.comment = comment
        self.vote_num = vote_num
        self.ulf_flg = ulf_flg
        self.to_vote = to_vote
        self.to_vote2 = to_vote2
        self.prepare_flg = prepare_flg

    def __repr__(self):
        #return '<UserName: %r  ' % (self.username)
        return f"id = {self.id}, username={self.username}"


class OtherVar(db2.Model):
    __tablename__ = 'OtherVariable'
    id = db.Column(db.Integer, primary_key=True)
    word_num = db.Column(db.Integer, nullable=False)
    global_ulfnum = db.Column(db.Integer, nullable=False)
    wolf_number = db.Column(db.Integer, nullable=False)
    genre_number = db.Column(db.Integer, nullable=False)
    word_ulf = db.Column(db.String(128), nullable=False)
    word_shimin = db.Column(db.String(128), nullable=False)
    quest1 = db.Column(db.String(256), nullable=True)
    quest2 = db.Column(db.String(256), nullable=True)
    quest3 = db.Column(db.String(256), nullable=True)
    quest4 = db.Column(db.String(256), nullable=True)
    quest5 = db.Column(db.String(256), nullable=True)

    def __init__(self, word_num = 0 , global_ulfnum = 0 ,wolf_number = 0 ,genre_number = 0 ,word_ulf = '' ,word_shimin = '',quest1 = '',quest2 = '',quest3 = '',quest4 = '',quest5 = ''):
        self.word_num = word_num
        self.global_ulfnum = global_ulfnum
        self.wolf_number = wolf_number
        self.genre_number = genre_number
        self.word_ulf = word_ulf
        self.word_shimin = word_shimin
        self.quest1 = quest1
        self.quest2 = quest2
        self.quest3 = quest3
        self.quest4 = quest4
        self.quest5 = quest5
        

    def __repr__(self):
        return f"id = {self.id},word_num = {self.word_num}, global_ulfnum={self.global_ulfnum}, word_ulf = {self.word_ulf}"


class OrignalGenreData(db3.Model):
    __tablename__ = 'OrignalGenreData'
    id = db3.Column(db.Integer, primary_key=True)
    GenreData = db.Column(db.String(128), nullable=True)

    def __init__(self, GenreData=None):
        self.GenreData = GenreData

    def __repr__(self):
        return f"{self.GenreData}"
