from maubot import Plugin
from sqlalchemy import *
from sqlalchemy.engine.base import Engine


class Database:
    plugin: Plugin
    db: Engine

    def __init__(self, db: Engine, plugin: Plugin) -> None:
        self.db = db
        self.plugin = plugin
        meta = MetaData()
        meta.bind = db

        self.messages = Table("messages", meta,
                              Column("id", Integer, primary_key=True, autoincrement=True),
                              Column("mrx_room_id", String(255), nullable=False),
                              Column("mrx_id", String(255), nullable=False, unique=True),
                              Column("external_id", String(255), nullable=False, unique=True)
                              )

        meta.create_all()

    def add_message(self, mrx_room_id: str, mrx_id: str, external_id: str) -> None:
        self.messages.insert().values(mrx_room_id=mrx_room_id, mrx_id=mrx_id, external_id=external_id).execute()

    def get_message_mrx_id(self, external_id: str) -> str:
        return self.messages.select(self.messages.c.external_id == external_id).execute().fetchone()["mrx_id"]
