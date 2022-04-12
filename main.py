import json
import os.path
import bcrypt

from server import App
from server.api import ApiModule
from server.config import ConfigModule
from server.db.sqlalchemy import SqlAlchemyModule
from server.job import JobModule

def main():
    app = App()

    if not os.path.exists("./config.json"):
        config = {
            "port": 13337,
            "debug": False,
            "salt": bcrypt.gensalt().decode()
        }
        with open("./config.json", "w") as h:
            h.write(json.dumps(config))
    else:
        with open("./config.json") as h:
            config = json.loads(h.read())

    app.register_module(ConfigModule, debug=config["debug"], salt=config["salt"].encode(), port=config["port"])
    app.register_module(SqlAlchemyModule)
    app.register_module(JobModule)
    app.register_module(ApiModule)

    app.run()

if __name__ == "__main__":
    main()
