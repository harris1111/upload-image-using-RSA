from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import false, true

from __init__ import db

class UserLoginModel(db.Model, UserMixin):
    __tablename__ = 'userlogin'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname=  Column(String(50) , nullable=False)
    username = Column(String(50) , nullable=False, unique=True)
    password = Column(Text, nullable=False)
    key_e = Column(Text, nullable=False)
    key_n = Column(Text, nullable=False)
    shares = relationship("SharePictureModel",backref="userlogin",lazy = True,cascade="delete")
    pictures = relationship("PictureModel",backref="userlogin",lazy = True,cascade="delete")
    def __str__(self):
        return "user"+str(self.id)
    
class PictureModel(db.Model):
    __tablename__ = 'picture'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_at = Column(DateTime, default = datetime.now(), nullable=False)
    pic = Column(Text)
    userlogin_id = Column(Integer, ForeignKey('userlogin.id'))
    shares = relationship("SharePictureModel",backref="picture",lazy = True,cascade="delete")
    def __str__(self):
        return "pic"+str(self.id)
    
class SharePictureModel(db.Model):
    __tablename__ = 'sharepicture'
    id = Column(Integer, primary_key=True, autoincrement=True)
    picture_id = Column(Integer, ForeignKey('picture.id'))
    userlogin_id = Column(Integer, ForeignKey('userlogin.id'))
    __table_args__ = (db.UniqueConstraint(picture_id, userlogin_id),)
    def __str__(self):
        return "share"+str(self.id)

if __name__=="__main__":
    db.create_all()
    pic = PictureModel.query.all()
    for i in pic:
        db.session.delete(i)
    db.session.commit()