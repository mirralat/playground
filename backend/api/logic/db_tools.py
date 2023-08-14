import uuid
from abc import abstractmethod, ABC
from uuid import UUID

import pydantic
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Column, String, Boolean
from sqlalchemy.testing.schema import Table
from sqlalchemy.dialects.postgresql import UUID

from backend.api.schemas import ValidUser
from backend.postgresql.models.user import User

engine = create_engine("postgresql://postgres:12345@127.0.0.1:5432/user_data")
conn = engine.connect()
metadata = MetaData()

UserTab = Table('users', metadata,
                Column('id', UUID, primary_key=True),
                Column('name', String),
                Column('password', String),
                Column('picture', String),
                Column('_User__isAdmin', Boolean)
                )


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
            new_id = uuid.uuid4()
            user = ValidUser(id=new_id, name=data['name'], password=data['password'], picture=data['picture'])
        except pydantic.error_wrappers.ValidationError:
            return False
        create = sqlalchemy.insert(UserTab).values(id=user.id, name=data['name'], password=data['password'],
                                                   picture=data['picture'], _User__isAdmin=False)
        conn.execute(create)
        print(conn.execute(sqlalchemy.select(UserTab).where(UserTab.id == new_id)))
        return True

    def updateUser(self, user_id, new_fields=dict) -> bool:
        user_to_update = conn.execute(sqlalchemy.select(User).where(id=user_id))

        if user_to_update:
            try:
                validation = ValidUser(name=new_fields['name'], password=['password'], picture=['picture'],
                                       _User__isAdmin=False)
            except pydantic.error_wrappers.ValidationError:
                return False
        else:
            return False

        update = db.update(User).where(id=user_id).values(name=new_fields['name'], password=['password'],
                                                          picture=['picture'])
        conn.execute(update)
        return True

    def deleteUser(self, user_id) -> bool:
        user_to_delete = conn.execute(sqlalchemy.select(User).where(id=user_id))
        if user_to_delete:
            delete = sqlalchemy.delete(User).where(id=user_id)
            conn.execute(delete)
            return True
        else:
            return False
