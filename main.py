# -*- coding: utf-8 -*-
import asyncio
import signal
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, Application

from config import conf
from config import logger
import controller
import model

chat_pool = model.ChatPool()


async def chat_handler(queue: asyncio.Queue, chat_id: int, chat_timeout: int) -> None:
    """
    处理聊天队列中的更新，直到超时
    """
    logger.info("new chat_handler: %d", chat_id)
    while True:
        try:
            update_config: model.UpdateConfig = await asyncio.wait_for(queue.get(), timeout=chat_timeout)
            await controller.Controller(update_config)
        except asyncio.exceptions.TimeoutError:
            logger.warning("chat_handler exited: %d", chat_id)
            await chat_pool.del_chat(chat_id)
            return
        except Exception as e:
            logger.exception(e)
            continue


async def update_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    1.更新分类
    2.根据聊天 ID 创建一个异步的聊天处理器，聊天处理器不允许并发，群组聊天48小时超时，私人聊天60秒超时
    3.新更新通过队列发送给聊天处理函数
    """
    update_type = model.MESSAGE_TYPE
    chat_type = ""
    chat_id = 0
    if update.message is not None:
        update_type = model.MESSAGE_TYPE
        chat_type = update.message.chat.type
        chat_id = update.message.chat_id

    if update.callback_query is not None:
        update_type = model.CALLBACK_QUERY_TYPE
        chat_type = update.callback_query.message.chat.type
        chat_id = update.callback_query.message.chat_id

    if update.inline_query is not None:
        update_type = model.INLINE_QUERY_TYPE
        chat_type = update.inline_query.chat_type
        chat_id = update.inline_query.from_user.id

    if chat_pool.is_chat_exist(chat_id):
        queue = chat_pool.get_chat(chat_id)
        await queue.put(model.UpdateConfig(update, context, update_type, chat_type, chat_id))
    else:
        queue = asyncio.Queue()
        chat_pool.add_chat(chat_id, queue)
        chat_timeout = 60 * 60 * 48
        if chat_type == "private":
            chat_timeout = 60
        asyncio.create_task(chat_handler(queue, chat_id, chat_timeout))
        await queue.put(model.UpdateConfig(update, context, update_type, chat_type, chat_id))


def main():
    # 启动 Bot
    app = ApplicationBuilder().token(conf.get_bot_token()).build()
    app.add_handler(MessageHandler(filters=filters.ALL, callback=update_handler))
    app.run_polling(close_loop=False)


def exit_handler(signum, frame):
    logger.info('shutdown bot by os signal %d', signum)
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, exit_handler)
    main()
