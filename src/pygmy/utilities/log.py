import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(name, level, filename,
                 fmt='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S',
                 propagate=False):
    logger = logging.getLogger(name)
    formatter = logging.Formatter(fmt)
    handler = TimedRotatingFileHandler(filename, 'midnight', backupCount=30, utc=True)
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = propagate
    return logger


logger = setup_logger('pygmy.log', logging.DEBUG, '/tmp/log/pygmy.log')
hadoop_logger = setup_logger(
        'pygmy.hadoop',
        logging.DEBUG,
        '/tmp/log/hadoop/hadoop.mail.click.log',
        fmt='%(message)s')


def log2hadoop(task_id, user_id, ip, device, os, browser, request_uri, referer, user_agent):
    pass
