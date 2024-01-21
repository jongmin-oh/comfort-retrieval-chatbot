import logging
import json


# JSON Formatter 설정
class ErrorFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'level': record.levelname,
            'code': record.code,
            'type': record.type,
            'message': record.msg
        }
        return json.dumps(log_data)


class Loggers:
    def create_logger(self, name, formatter, handler):
        logger = logging.getLogger(name)

        if len(logger.handlers) > 0:
            return logger

        logger.setLevel(logging.DEBUG)

        handler.setLevel(logging.DEBUG)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    def get_console_logger(self):
        formatter = logging.Formatter("[%(levelname)s] %(asctime)s > %(message)s")
        stream_handler = logging.StreamHandler()
        return self.create_logger("Stream", formatter, stream_handler)

    def get_error_logger(self):
        formatter = ErrorFormatter()
        stream_handler = logging.StreamHandler()
        return self.create_logger("Error", formatter, stream_handler)

    def get_file_logger(self):
        formatter = logging.Formatter("%(message)s")
        file_handler = logging.FileHandler("logs/log.log")
        return  self.create_logger("file", formatter, file_handler)


console_logger = Loggers().get_console_logger()
error_logger = Loggers().get_error_logger()