# -*- coding: utf-8 -*-
import logging
import os

import yaml

logger = logging.getLogger('BOT')
_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
_stream_handler = logging.StreamHandler()
_stream_handler.setFormatter(_formatter)
logger.addHandler(_stream_handler)


class Config:
    __config: dict

    def __init__(self) -> None:
        config_file = os.getenv('BOT_CONFIG')
        with open(file=config_file, mode='r', encoding='utf-8') as f:
            self.__config = yaml.load(stream=f, Loader=yaml.FullLoader)

        log_level = self.__config.get('log_level')

        match log_level:
            case 0, 1:
                logger.setLevel(logging.ERROR)
            case 2:
                logger.setLevel(logging.INFO)
            case 3:
                logger.setLevel(logging.DEBUG)
            case log_level if log_level > 3:
                logger.setLevel(logging.DEBUG)
                logging.basicConfig(level=logging.DEBUG)

        logger.debug(f'load config {self.__config}')

    def get_config(self) -> dict:
        return self.__config

    def get_bot_token(self) -> str:
        return self.__config.get('bot_token')

    def get_log_level(self) -> int:
        return self.__config.get('log_level')


conf = Config()
