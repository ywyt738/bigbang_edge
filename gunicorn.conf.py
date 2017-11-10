import logging
import logging.handlers

bind = "127.0.0.1:8000"
workers = 1
chdir = "/usr/local/src/bigbang_edge"
raw_env = ['DJANGO_PRODUCTION=True']
accesslog = "/dev/null"

acclogger = logging.getLogger('gunicorn.access')
errlogger = logging.getLogger('gunicorn.error')
acclogger.propagate = False
errlogger.propagate = False
acc_handler = logging.handlers.TimedRotatingFileHandler(
    r'/var/log/bigbang/accesslog', 'D', 1, 30)
err_handler = logging.handlers.TimedRotatingFileHandler(
    r'/var/log/bigbang/errorlog', 'D', 1, 30)
acc_handler.suffix = '%Y-%m-%d.log'
err_handler.suffix = '%Y-%m-%d.log'
acclogger.addHandler(acc_handler)
errlogger.addHandler(err_handler)
