# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present EVG
"""

import os
from datetime import timedelta

from decouple import config
from celery.schedules import crontab


class Config(object):

    # Set up the Telegram Bot
    TELEGRAM_BOT_CHAT_API_URL = config('TELEGRAM_BOT_CHAT_API_URL')
    TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
    TELEGRAM_BOT_CHATID = config('TELEGRAM_BOT_CHATID')
    TELEGRAM_TAG = config('TELEGRAM_TAG')

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY')

    TIMEZONE = config("TIMEZONE", default="Asia/Ho_Chi_Minh")

    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(
        config("DB_ENGINE"),
        config("DB_USERNAME"),
        config("DB_PASS"),
        config("DB_HOST"),
        config("DB_PORT"),
        config("DB_NAME"),
    )
    SQLALCHEMY_ENGINE_OPTIONS = {
        "echo_pool": True
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ANTMEDIA_URI = config("ANTMEDIA_URI")
    ANTMEDIA_USER = config("ANTMEDIA_USER")
    ANTMEDIA_PASSWORD = config("ANTMEDIA_PASSWORD")

    CELERY_BROKER_URL = config("CELERY_BROKER_URL")
    CELERYBEAT_SCHEDULE = {
        # Executes every minute
        'periodic_task-every-minute': {
            'task': 'periodic_task',
            # 'schedule': crontab(minute="*")
            'schedule': timedelta(seconds=2)
        },
        'periodic_app_task-every-minute': {
            'task': 'periodic_app_task',
            # 'schedule': crontab(minute="*")
            'schedule': timedelta(seconds=2)
        },
        'periodic_event_log_task-every-minute': {
            'task': 'periodic_event_log_task',
            # 'schedule': crontab(minute="*")
            'schedule': timedelta(seconds=5)
        },
    }
    CELERY_EVENT_WORKERS = config("CELERY_EVENT_WORKERS")
    CELERY_EVENT_WORKERS = CELERY_EVENT_WORKERS.split(',')
    CELERY_ROUTES = {
        'apps.worker.tasks.event_handle_worker_1': {'queue': 'event_handle_worker_1'},
        'apps.worker.tasks.event_handle_worker_2': {'queue': 'event_handle_worker_2'},
        'apps.worker.tasks.event_handle_worker_3': {'queue': 'event_handle_worker_3'},
        'apps.worker.tasks.event_handle_worker_4': {'queue': 'event_handle_worker_4'},
        'apps.worker.tasks.event_handle_worker_5': {'queue': 'event_handle_worker_5'},
        'apps.worker.tasks.worker_1': {'queue': 'worker_1'},
        'apps.worker.tasks.worker_2': {'queue': 'worker_2'},
    }

    # S3_AGENT_ENDPOINTS = config("S3_AGENT_ENDPOINTS").split(',')
    S3_AGENT_ENDPOINTS = ['127.0.0.1/api/v1/event', '192.168.9.3/api/v1/event']


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {"Production": ProductionConfig, "Debug": DebugConfig}
