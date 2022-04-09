from server import App
from server.api import ApiModule
from server.config import ConfigModule
from server.db.sqlalchemy import SqlAlchemyModule

def main():
    app = App()

    app.register_module(ConfigModule, debug=True)
    app.register_module(SqlAlchemyModule)
    app.register_module(ApiModule)

    app.run()

if __name__ == "__main__":
    main()
