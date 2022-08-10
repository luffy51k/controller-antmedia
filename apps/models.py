# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present EVG
"""

import datetime
import pytz
from apps import db

TIMEZONE = 'Asia/Ho_Chi_Minh'


class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    webrtc_enable = db.Column(db.Integer, nullable=False)
    adaptive_enable = db.Column(db.Integer, nullable=False)
    adaptive_profiles = db.Column(db.TEXT, nullable=True)
    enable_record_mp4 = db.Column(db.Integer, nullable=False)
    enable_add_datetime_record_mp4 = db.Column(db.Integer, nullable=False)
    s3_enable = db.Column(db.Integer, nullable=False)
    s3_storage_id = db.Column(db.Integer, nullable=True)
    webhook_url = db.Column(db.String(64), nullable=True)  # Customer Registry Endpoint receive event
    # (Stream started, Stream end, Upload VoD Success)
    preview_enable = db.Column(db.Integer, nullable=False)
    app_setting = db.Column(db.JSON, nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), nullable=True)
    changed_on = db.Column(db.DateTime(timezone=True), nullable=True)
    deleted = db.Column(db.Integer, nullable=True)

    def __init__(self, name=None, user_id=None, status=None, webrtc_enable=None, adaptive_enable=None,
                 adaptive_profiles=None, enable_record_mp4=None, enable_add_datetime_record_mp4=None,
                 s3_enable=None, s3_storage_id=None, webhook_url=None, preview_enable=None, app_setting=None,
                 created_on=None, changed_on=None):
        self.name = name
        self.user_id = user_id
        self.status = status
        self.webrtc_enable = webrtc_enable
        self.adaptive_enable = adaptive_enable
        self.adaptive_profiles = adaptive_profiles
        self.enable_record_mp4 = enable_record_mp4
        self.enable_add_datetime_record_mp4 = enable_add_datetime_record_mp4
        self.s3_enable = s3_enable
        self.s3_storage_id = s3_storage_id
        self.webhook_url = webhook_url
        self.preview_enable = preview_enable
        self.app_setting = app_setting
        self.created_on = created_on
        self.changed_on = changed_on

    def __repr__(self):
        return "<App {0}>".format(self.name)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'status': self.status,
            'webrtc_enable': self.webrtc_enable,
            'adaptive_enable': self.adaptive_enable,
            'adaptive_profiles': self.adaptive_profiles,
            'enable_record_mp4': self.enable_record_mp4,
            'enable_add_datetime_record_mp4': self.enable_add_datetime_record_mp4,
            's3_enable': self.s3_enable,
            's3_storage_id': self.s3_storage_id,
            'webhook_url': self.webhook_url,
            'preview_enable': self.preview_enable,
            'app_setting': self.app_setting,
            'created_on': self.created_on,
            'changed_on': self.changed_on,
            'deleted': self.deleted
        }


class LiveStream(db.Model):
    __tablename__ = "livestream"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    stream_id = db.Column(db.String(64), unique=True, nullable=False)
    publish_url = db.Column(db.String(64), nullable=True)
    hls_playback = db.Column(db.String(64), nullable=True)
    status = db.Column(db.Integer, nullable=True)  # 0: Normal; -1: Lock
    streaming_status = db.Column(db.String(64), nullable=True)  # 0: Offline, 1: Broadcasting
    type = db.Column(db.String(64), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    live_setting = db.Column(db.JSON, nullable=True)
    application_id = db.Column(db.Integer, db.ForeignKey(
        "application.id"), nullable=False)
    application = db.relationship('Application', backref='LiveStream', lazy=True)
    event_enable = db.Column(db.Integer, nullable=True)
    event_start_on = db.Column(db.DateTime(timezone=True), nullable=True)
    event_finish_on = db.Column(db.DateTime(timezone=True), nullable=True)
    transcoding_enable = db.Column(db.Integer, nullable=True)
    publish_token = db.Column(db.String(64), nullable=True)
    created_on = db.Column(db.DateTime(timezone=True), nullable=True)
    changed_on = db.Column(db.DateTime(timezone=True), nullable=True)
    deleted = db.Column(db.Integer, nullable=True)

    def __init__(self, name=None, stream_id=None, publish_url=None, hls_playback=None, event_start_on=None,
                 event_finish_on=None, status=None, streaming_status=None, type=None, duration=None,
                 live_setting=None, application_id=None, created_on=None, changed_on=None,
                 event_enable=None, transcoding_enable=None, publish_token=None):
        self.name = name
        self.stream_id = stream_id
        self.publish_url = publish_url
        self.hls_playback = hls_playback
        self.event_start_on = event_start_on  # time starting that allow push stream
        self.event_finish_on = event_finish_on  # time finishing that allow push stream
        self.status = status
        self.streaming_status = streaming_status
        self.type = type
        self.duration = duration  # duration livestream / session id newest
        self.live_setting = live_setting
        self.application_id = application_id
        self.created_on = created_on
        self.changed_on = changed_on
        self.event_enable = event_enable
        self.transcoding_enable = transcoding_enable
        self.publish_token = publish_token

    def __repr__(self):
        return "<LiveStream {0}>".format(self.stream_id)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'stream_id': self.stream_id,
            'publish_url': self.publish_url,
            'hls_playback': self.hls_playback,
            'event_start_on': self.event_start_on,
            'event_finish_on': self.event_finish_on,
            'status': self.status,
            'streaming_status': self.streaming_status,
            'type': self.type,
            'duration': self.duration,
            'live_setting': self.live_setting,
            'application_id': self.application_id,
            'application': self.application.to_json(),
            'created_on': self.created_on,
            'changed_on': self.changed_on,
            'publish_token': self.publish_token,
            'deleted': self.deleted
        }


class StreamingHistory(db.Model):
    __tablename__ = "streaming_history"

    id = db.Column(db.Integer, primary_key=True)
    livestream_id = db.Column(db.Integer, db.ForeignKey(
        "livestream.id"), nullable=False)
    livestream = db.relationship('LiveStream', backref='StreamingHistory', lazy=True)
    start_time = db.Column(db.DateTime(timezone=True), nullable=True)
    end_time = db.Column(db.DateTime(timezone=True), nullable=True)
    session_id = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(64), nullable=True)
    stats = db.Column(db.TEXT, nullable=True)
    vod_id = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Integer, nullable=True)
    created_on = db.Column(db.DateTime(timezone=True), nullable=True)
    changed_on = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, livestream_id=None, start_time=None, end_time=None, state=None,
                 stats=None, session_id=None, vod_id=None, completed=None, created_on=None, changed_on=None):
        self.livestream_id = livestream_id
        self.start_time = start_time
        self.end_time = end_time
        self.state = state
        self.stats = stats
        self.session_id = session_id
        self.vod_id = vod_id
        self.completed = completed
        self.created_on = created_on
        self.changed_on = changed_on

    def __repr__(self):
        return "<StreamingHistory {0}>".format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'livestream_id': self.livestream_id,
            'livestream': self.livestream.to_json(),
            'start_time': self.start_time,
            'end_time': self.end_time,
            'state': self.state,
            'stats': self.stats,
            'session_id': self.session_id,
            'vod_id': self.vod_id,
            'completed': self.completed,
            'created_on': self.created_on,
            'changed_on': self.changed_on
        }


class S3Storage(db.Model):
    __tablename__ = "s3_storage"

    id = db.Column(db.Integer, primary_key=True)
    s3_endpoint = db.Column(db.String(64), nullable=True)
    s3_bucket = db.Column(db.String(64), nullable=True)
    s3_secret_key = db.Column(db.String(64), nullable=True)
    s3_access_key = db.Column(db.String(64), nullable=True)
    s3_enable_tls = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)

    def __init__(self, s3_endpoint=None, s3_bucket=None, s3_secret_key=None, s3_access_key=None,
                 s3_enable_tls=None, user_id=None, status=None):
        self.s3_endpoint = s3_endpoint
        self.s3_bucket = s3_bucket
        self.s3_secret_key = s3_secret_key
        self.s3_access_key = s3_access_key
        self.s3_enable_tls = s3_enable_tls
        self.user_id = user_id
        self.status = status

    def __repr__(self):
        return "<S3Storage {0}>".format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            's3_endpoint': self.s3_endpoint,
            's3_bucket': self.s3_bucket,
            's3_secret_key': self.s3_secret_key,
            's3_access_key': self.s3_access_key,
            's3_enable_tls': self.s3_enable_tls,
            'user_id': self.user_id,
            'status': self.status

        }


class Vod(db.Model):
    __tablename__ = "vod"

    id = db.Column(db.Integer, primary_key=True)
    livestream_id = db.Column(db.Integer, db.ForeignKey(
        "livestream.id"), nullable=False)
    livestream = db.relationship('LiveStream', backref='Vod', lazy=True)
    start_time = db.Column(db.DateTime(timezone=True), nullable=True)
    end_time = db.Column(db.DateTime(timezone=True), nullable=True)
    s3_link = db.Column(db.String(64), nullable=True)
    hls_link = db.Column(db.String(64), nullable=True)
    session_id = db.Column(db.String(64), nullable=True)
    antmedia_vod_id = db.Column(db.String(64), nullable=True)
    created_on = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return "<Vod {0}>".format(self.id)

    def to_json(self, livestream_id=None, start_time=None, end_time=None, s3_link=None, hls_link=None,
                antmedia_vod_id=None,
                session_id=None, created_on=None):
        self.livestream_id = livestream_id
        self.start_time = start_time
        self.end_time = end_time
        self.s3_link = s3_link
        self.hls_link = hls_link
        self.session_id = session_id
        self.antmedia_vod_id = antmedia_vod_id
        self.created_on = created_on


class S3SyncHistory(db.Model):
    __tablename__ = "s3_sync_history"

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(64), nullable=True)
    s3_endpoint = db.Column(db.String(64), nullable=True)
    s3_bucket = db.Column(db.String(64), nullable=True)
    s3_secret_key = db.Column(db.String(64), nullable=True)
    s3_access_key = db.Column(db.String(64), nullable=True)
    s3_secure = db.Column(db.Integer, nullable=True)
    livestream_id = db.Column(db.Integer, db.ForeignKey(
        "livestream.id"), nullable=False)
    livestream = db.relationship('LiveStream', backref='S3SyncHistory', lazy=True)
    status = db.Column(db.Integer, nullable=True)
    retry_counter = db.Column(db.Integer, nullable=True)
    session_id = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        return "<S3SyncHistory {0}>".format(self.id)

    def to_json(self, file_path=None, s3_endpoint=None, s3_bucket=None, s3_secret_key=None, s3_access_key=None,
                s3_secure=None, livestream_id=None, status=None, retry_counter=None, session_id=None):
        self.file_path = file_path
        self.s3_endpoint = s3_endpoint
        self.s3_bucket = s3_bucket
        self.s3_secret_key = s3_secret_key
        self.s3_access_key = s3_access_key
        self.s3_secure = s3_secure
        self.livestream_id = livestream_id
        self.status = status
        self.retry_counter = retry_counter
        self.session_id = session_id


class EventLog(db.Model):
    __tablename__ = "event_log"

    id = db.Column(db.Integer, primary_key=True)
    stream_id = db.Column(db.String(64), nullable=True)
    action = db.Column(db.String(64), nullable=True)
    event = db.Column(db.JSON, nullable=True)
    worker_queue = db.Column(db.String(64), nullable=True)
    status = db.Column(db.Integer, nullable=False, default=8)
    reason_error = db.Column(db.TEXT, nullable=True)
    created_on = db.Column(db.DateTime(timezone=True), nullable=True)
    changed_on = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return "<EventLog {0}>".format(self.id)

    def to_json(self, stream_id=None, action=None, event=None, worker_queue=None,
                status=None, reason_error=None, created_on=None, changed_on=None):
        self.stream_id = stream_id
        self.action = action
        self.event = event
        self.worker_queue = worker_queue
        self.status = status
        self.reason_error = reason_error
        self.created_on = created_on
        self.changed_on = changed_on

