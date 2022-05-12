from maubot import Plugin
from maubot.matrix import parse_formatted
from mautrix.types import MessageType, EventType, TextMessageEventContent, Format, EventID
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from typing import Type
import asyncio
import socketio

from .db import Database


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("api_key")
        helper.copy("api_uri")
        helper.copy("room_map")


class MsgPipeline(Plugin):
    db: Database

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    async def start(self) -> None:
        self.log.debug('startup')
        await super().start()
        self.config.load_and_update()
        self.db = Database(self.database, self)
        asyncio.ensure_future(self.websocket())

    async def websocket(self) -> None:
        api_uri = self.config["api_uri"]
        api_key = self.config["api_key"]

        room_config = self.config["room_map"]
        room_map = {}
        for r in room_config:
            for external_id, matrix_id in r.items():
                room_map[external_id] = matrix_id

        if api_uri == "" or api_key == "":
            self.log.error("API URI or API key is empty")
            return

        sio = socketio.AsyncClient()

        @sio.on('message')
        async def on_message(data):
            self.log.debug(data)
            mrx_id = room_map.get(data["room"])
            if mrx_id is None:
                self.log.debug("Room not found in config: " + data["room"])
            else:
                if mrx_id.startswith("#"):
                    alias = await self.client.resolve_room_alias(mrx_id)
                    mrx_id = alias.room_id

                if data["type"] == "message":
                    await send_message(data, mrx_id)
                elif data["type"] == "delete":
                    await delete_message(data, mrx_id)

        async def send_message(data, mrx_id):
            if data["reply"] is None or data["reply"] == "":
                msg_event_id = await self.client.send_markdown(room_id=mrx_id,
                                                               markdown=data["message"],
                                                               msgtype=MessageType.TEXT)
            else:
                content = TextMessageEventContent(msgtype=MessageType.TEXT, format=Format.HTML)
                content.body, content.formatted_body = await parse_formatted(data["message"])
                reply_event = self.db.get_message_mrx_id(data["reply"])
                self.log.debug(reply_event)
                if reply_event is not None:
                    content.set_reply(EventID(reply_event))
                msg_event_id = await self.client.send_message_event(room_id=mrx_id,
                                                                    event_type=EventType.ROOM_MESSAGE,
                                                                    content=content)
            self.log.debug("Message sent: " + msg_event_id)
            self.db.add_message(mrx_room_id=mrx_id, mrx_id=msg_event_id, external_id=data["event_id"])

        async def delete_message(data, mrx_id):
            event_id = EventID(self.db.get_message_mrx_id(data["event_id"]))
            await self.client.redact(room_id=mrx_id, event_id=event_id, reason="Deleted via MSG Pipeline")

        @sio.event()
        def connect():
            self.log.info('Connected to Websocket as: ' + sio.sid)

        @sio.event()
        def disconnect():
            self.log.info("Disconnected from Websocket")

        await sio.connect(api_uri, auth=api_key)
        await sio.wait()
