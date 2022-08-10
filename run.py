# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present EVG
"""
from apps import DEBUG, app, app_config, get_config_mode, celery_app

if DEBUG:
    app.logger.info("DEBUG       = " + str(DEBUG))
    app.logger.info("Environment = " + get_config_mode)
    app.logger.info("DBMS        = " + app_config.SQLALCHEMY_DATABASE_URI)

celery = celery_app

if __name__ == "__main__":
    app.run(host='0.0.0.0')
