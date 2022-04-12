from multiprocessing import Process
import time
from typing import List

from ..app import App
from ..db import DBModule
from ..db.objects.server import ServerObject
from ..module import Module

def server_ping_process(db: DBModule):
    while True:
        time.sleep(60)
        servers = db.get_all(ServerObject)

        for server in servers:
            if not server.ping():
                db.delete(ServerObject, server.id)

class JobModule(Module):
    __db: DBModule
    __processes: List[Process]

    def __init__(self, app: App):
        self.__db = app.load_module(DBModule)
        self.__processes = []

    def __del__(self):
        for process in self.__processes:
            process.terminate()

    def run(self):
        self.__processes = [
            Process(target=server_ping_process, args=(self.__db,))
        ]

        for process in self.__processes:
            process.start()
