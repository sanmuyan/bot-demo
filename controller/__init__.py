# -*- coding: utf-8 -*-
import model
from config import logger
from service import CommandConfig


async def Controller(update_config: model.UpdateConfig) -> None:
    """
    分发处理逻辑
    """
    logger.debug(update_config.update)
    match update_config.update_type:
        case model.MESSAGE_TYPE:
            if update_config.is_command():
                command_config = CommandConfig(update_config.update, update_config.context)
                await command_config.in_commands()
        case model.CALLBACK_QUERY_TYPE:
            pass
        case model.INLINE_QUERY_TYPE:
            pass
