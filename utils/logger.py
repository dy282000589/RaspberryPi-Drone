import logging

class Logger:
    def __init__(self, log_file='drone.log'):
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger()

    def log(self, message):
        self.logger.info(message)
        print(message)
