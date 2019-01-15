# coding=utf-8

import datetime as dt

from apps.web.extensions import db

Model = db.Model
relationship = db.relationship
ForeignKey = db.ForeignKey
Column = db.Column
Integer = db.Integer
String = db.String
Boolean = db.Boolean
DateTime = db.DateTime


class Task(Model):
    """任务"""
    __tablename__ = 'task'
    task_id = Column(Integer, primary_key=True)
    task_uuid = Column(String(128), nullable=False, default='')
    name = Column(String(128), nullable=False, default='')
    state = Column(String(16), nullable=False, default='')

    create_datetime = Column(DateTime, nullable=False, default=dt.datetime.now)
    start_datetime = Column(DateTime, nullable=True)
    finish_datetime = Column(DateTime, nullable=True)

    @property
    def id(self):
        return self.task_id

    @id.setter
    def id(self, value):
        self.task_id = value

    @property
    def uuid(self):
        return self.task_uuid

    @uuid.setter
    def uuid(self, value):
        self.task_uuid = value

    def get_result(self):
        pass

    def to_dict(self):
        d = dict(
            id=self.task_id,
            type_id=self.task_type_id,
            name=self.name,
            create_datetime=dt.datetime.strftime(self.create_datetime, '%Y-%m-%d %H:%M:%S'),
            start_datetime=self.start_datetime or '',
            finish_datetime=self.finish_datetime or ''
        )
        return d
