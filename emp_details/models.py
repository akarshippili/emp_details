from tracemalloc import start
from typing import Sequence
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Department(Base):
    __tablename__ = 'departments'
    # composite primary keys are not supported in sqlite
    id = Column(Integer)
    name = Column(String(50), primary_key=True)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Department {self.name!r}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)
    department = Column(String(50), ForeignKey('departments.name'))
    created_at = Column(TIMESTAMP, server_default=func.now())

    # department = relationship(
    #     'Department', primaryjoin='User.department==Department.name', backref='users')

    def __init__(self, name=None, email=None, department=None):
        self.name = name
        self.email = email
        self.department = department

    def __repr__(self):
        return f'<User {self.name!r}>'

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'created_at': self.created_at
        }
