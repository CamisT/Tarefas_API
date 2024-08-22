import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        if not app.logger.handlers:
            handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
            handler.setFormatter(formatter)
            app.logger.addHandler(handler)
