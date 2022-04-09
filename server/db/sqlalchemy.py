from typing import List, Type
import sqlalchemy

from server.db.objects.base import DBString

from .objects import DBObject
from ..app import App
from . import DBModule

class SqlAlchemyModule(DBModule):
    __engine: sqlalchemy.engine.Engine
    __metadata: sqlalchemy.MetaData
    
    def __init__(self, app: App):
        self.__engine = sqlalchemy.create_engine("sqlite:///server.db")
        self.__metadata = sqlalchemy.MetaData()
        DBModule.__init__(self, app)

    def register_objects(self, types: List[Type[DBObject]]):
        for type in types:
            collection = type.get_collection_name()
            fields = type.get_fields()

            columns: List[sqlalchemy.Column] = [
                sqlalchemy.Column("id", sqlalchemy.Integer())
            ]

            for field_name, field in fields.items():
                if isinstance(field, DBString):
                    column = sqlalchemy.Column(field_name, sqlalchemy.String())
                else:
                    raise Exception(f"Unhandled {field}")

                columns.append(column)

            sqlalchemy.Table(collection, self.__metadata, *columns)

        self.__metadata.create_all(self.__engine)

    def get_all(self, type: Type[DBObject]) -> List[DBObject]:
        with self.__engine.connect() as connection:
            table = sqlalchemy.Table(type.get_collection_name(), self.__metadata)
            query = sqlalchemy.select([table])
            proxy = connection.execute(query)
            results = proxy.fetchall()

        datas: List[DBObject] = []
        for fields in results:
            data = {}

            for field, field_name in zip(fields[1:], type.get_fields().keys()):
                data[field_name] = field

            datas.append(type(**data))

        return datas
