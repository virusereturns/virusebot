import logging

from datetime import datetime

import local_settings as settings


class Logger(object):
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            datefmt="%m-%d %H:%M:%S",
            filename=f"{settings.CHAT_LOG_FOLDER}chat{datetime.today().strftime('%Y-%m-%d')}.log",
            filemode="a",
        )
        self.logger = logging.getLogger("virusebot.logger.Logger")
        self.logger.info("Logger is now alive.")
        print("Logger is alive.")

    def log(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)
