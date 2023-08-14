from abc import abstractmethod, ABC

import pydantic
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker

from backend.api.schemas import ValidUser
from backend.postgresql.models.user import User

engine = db.create_engine("test")
Session = sessionmaker(bind=engine)
session = Session()


class UserInteractionsPattern(ABC):
    @abstractmethod
    def createUser(self, user_data) -> bool:
        pass

    @abstractmethod
    def updateUser(self, user_id, new_fields) -> bool:
        pass

    @abstractmethod
    def deleteUser(self, user_id) -> bool:
        pass


class UserInteractions(UserInteractionsPattern):
    def createUser(self, data=dict) -> bool:
        try:
            user = ValidUser(name=data['name'], password=data['password'], avatar=data['avatar'])
        except pydantic.error_wrappers.ValidationError:
            return False
        session.insert(User).values(name=data['name'], password=data['password'], avatar=data['avatar'])
        session.commit()
        return True

    def updateUser(self, user_id, new_fields=dict) -> bool:
        user_to_update = session.select(User).where(id=user_id)
        if user_to_update:
            try:
                validation = ValidUser(name=new_fields['name'], password=['password'], avatar=['avatar'])
            except pydantic.error_wrappers.ValidationError:
                return False
        else:
            return False

        session.update(user_to_update).values(name=new_fields['name'],
                                                         password=['password'], avatar=['avatar'])
        session.commit()
        return True

    def deleteUser(self, user_id) -> bool:
        user_to_delete = session.select(User).where(id=user_id)
        if user_to_delete:
            session.delete(user_to_delete)
            session.commit()
            return True
        else:
            return False

