import uuid

from sqlalchemy import Boolean, Column, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    picture = Column(LargeBinary, nullable=True)
    __isAdmin = Column(Boolean, nullable=False)

    @property
    def isAdmin(self) -> bool:
        if self.isAdmin:
            return True
        return False

    @isAdmin.setter
    def isAdmin(self, value):
        self.isAdmin = value

    def __setattr__(self, key, value):
        if key == 'isAdmin' and type(value) is bool:
            super().__setattr__(key, value)
