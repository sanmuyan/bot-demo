# -*- coding: utf-8 -*-
import asyncio

from telegram import Update
from telegram.ext import ContextTypes

MESSAGE_TYPE = "message"
CALLBACK_QUERY_TYPE = "callback_query"
INLINE_QUERY_TYPE = "inline_query"


class UpdateConfig:
    update: Update
    context: ContextTypes
    update_type: str
    chat_type: str
    chat_id: int

    def __init__(self, update: Update, context: ContextTypes, update_type: str, chat_type: str, chat_id: int):
        self.update = update
        self.context = context
        self.update_type = update_type
        self.chat_type = chat_type
        self.chat_id = chat_id

    def is_command(self) -> bool:
        if self.update_type != MESSAGE_TYPE:
            return False
        if len(self.update.message.entities) == 0:
            return False
        return self.update.message.entities[0].offset == 0 and self.update.message.entities[0].type == "bot_command"


class ChatPool:
    __pool = {}
    __lock = asyncio.Lock()

    def is_chat_exist(self, chat_id: int) -> bool:
        return chat_id in self.__pool

    def add_chat(self, chat_id: int, chat_queue: asyncio.Queue):
        self.__pool[chat_id] = chat_queue

    def get_chat(self, chat_id: int) -> asyncio.Queue:
        return self.__pool.get(chat_id)

    async def del_chat(self, chat_id: int):
        if self.is_chat_exist(chat_id):
            await self.__lock.acquire()
            del self.__pool[chat_id]
            self.__lock.release()
