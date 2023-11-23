# -*- coding: utf-8 -*-

from telegram import Update
from telegram.ext import ContextTypes


class BotConfig:
    """
    Bot 各类处理的基类
    """

    update: Update
    context: ContextTypes.DEFAULT_TYPE

    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context
