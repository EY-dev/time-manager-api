import logging
import os


class LoggerIt:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if LoggerIt.__instance is None:
            LoggerIt()
        return LoggerIt.__instance

    def __init__(self):
        if LoggerIt.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            LoggerIt.__instance = self
            __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            error_message = os.path.join(__location__, 'errors.log')
            info_message = os.path.join(__location__, 'info.log')
            self.error_logger = logging.getLogger('Time-Manager-API-Error')
            fh = logging.FileHandler(error_message)
            fh.setLevel(logging.ERROR)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.error_logger.addHandler(fh)

            self.info_logger = logging.getLogger('Time-Manager-API-Info')
            fh = logging.FileHandler(info_message)
            fh.setLevel(logging.WARNING)
            fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.info_logger.addHandler(fh)

    def write_error(self, msg='Something went wrong'):
        self.error_logger.error(msg)

    def write_info(self, msg='Everything goes normal'):
        self.info_logger.warning(msg)
