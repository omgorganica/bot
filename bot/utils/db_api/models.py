import datetime
from sqlalchemy import (Column, Integer, String, ForeignKey, Boolean, DateTime, func)
from sqlalchemy import sql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from utils.db_api.database import db

now = datetime.datetime.now()


class ShiftUser(db.Model):
    __tablename__ = 'adm_shiftuser'
    query: sql.Select
    id = Column(Integer, primary_key=True,nullable=True)
    name = Column(String(50))
    result = relationship('Result')

    def __repr__(self):
        return f'Пользователь {self.name} из смены {self.shift}'


class Question(db.Model):
    __tablename__ = 'adm_question'
    query: sql.Select
    id = Column(Integer, primary_key=True)
    text = Column(String(200))
    category = Column(String(200))
    result = relationship('Result')

    def __repr__(self):
        return self.text


class Shift(db.Model):
    __tablename__ = 'adm_shift'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey('adm_shiftuser.id'),nullable=True)
    score = Column(Integer,nullable=True)


class Result(db.Model):
    __tablename__ = 'adm_result'
    query = sql.Select
    id = Column(Integer, primary_key=True)
    # shift_id = Column(UUID)
    shift_id = Column(Integer, ForeignKey('adm_shift.id'))
    user_id = Column(Integer, ForeignKey('adm_shiftuser.id'))
    date = Column(DateTime(timezone=False), default=now)
    category = Column(String(255))
    question_id = Column(Integer, ForeignKey('adm_question.id'))
    result = Column(Boolean)
