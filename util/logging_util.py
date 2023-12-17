import logging

def initialize_logger():
    logging.basicConfig(
        filename='bot_logs.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
    )

def get_logger(name):
    return logging.getLogger(name)