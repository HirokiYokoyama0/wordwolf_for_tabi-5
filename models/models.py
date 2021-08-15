
from os import name
import os
from sqlalchemy import Column, Integer, String, Text, DateTime
# from models.database import Base
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


base_dir = os.path.dirname(__file__) #ファイルのパス

app = Flask(__name__)
# DataBaseの接続先を設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'userdata.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MemberList(db.Model):
    __tablename__ = 'memberlist'
    id = Column(Integer, primary_key=True)
    #username = Column(String(128), unique=True)
    username = Column(String(128))
    comment = Column(Text)
    date = Column(DateTime, default=datetime.now())

    def __init__(self, username=None, comment=None):
        self.username = username
        self.comment = comment
    

    def __repr__(self):
        #return '<UserName: %r  ' % (self.username)
        return f"id = {self.id}, username={self.username}, comment={self.comment}"
        