# -*- coding: utf-8 -*-
from telegram import Update
from telegram.ext import ContextTypes

from config import logger
from .bot import BotConfig


class CommandConfig(BotConfig):
    """
    处理 Bot 命令
    """
    command: str
    command_arg: str

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        super().__init__(update, context)
        command_full = update.message.text.removeprefix('/').replace('@' + self.context.bot.username, '').split(' ')
        self.command = command_full[0]
        if len(command_full) == 2:
            self.command_arg = command_full[1]

    async def in_commands(self):
        """
        分发命令
        """
        if self.command in commands_register:
            await commands_register[self.command](self)
        else:
            logger.warning('unknown command: %s', self.command)

    async def help_command(self):
        await self.update.message.reply_text('help')


commands_register = {
    "help": CommandConfig.help_command
}
