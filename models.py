from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(120), unique=True)
    department = Column(String(50))

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
            'department': self.department
        }
