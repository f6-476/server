from typing import List, Optional, Type
import sqlalchemy

from server.db.objects.base import DBInteger, DBString

from .objects import DBObject
from ..app import App
from . import TOBJ, DBModule

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
            fields = type.get_fields(self._config)

            columns: List[sqlalchemy.Column] = []

            for field_name, field in fields.items():
                if isinstance(field, DBString):
                    column = sqlalchemy.Column(field_name, sqlalchemy.String(), primary_key=field.primary)
                elif isinstance(field, DBInteger):
                    column = sqlalchemy.Column(field_name, sqlalchemy.Integer(), primary_key=field.primary)
                else:
                    raise Exception(f"Unhandled {field}")

                columns.append(column)

            sqlalchemy.Table(collection, self.__metadata, *columns)

        self.__metadata.create_all(self.__engine)

    def get_all(self, type: Type[TOBJ]) -> List[TOBJ]:
        with self.__engine.connect() as connection:
            table = sqlalchemy.Table(type.get_collection_name(), self.__metadata)
            query = sqlalchemy.select([table])
            proxy = connection.execute(query)
            results = proxy.fetchall()

        datas: List[TOBJ] = []
        for fields in results:
            data = {field_name:field for field_name, field in zip(type.get_fields(self._config).keys(), fields)}
            datas.append(type(**data))

        return datas

    def get_id(self, type: Type[TOBJ], id: str) -> Optional[TOBJ]:
        return None

    def insert(self, object: DBObject) -> bool:
        return False
