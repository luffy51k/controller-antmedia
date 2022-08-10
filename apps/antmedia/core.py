# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present EVG
"""
import json
import requests
from retry import retry
from antmedia_client.domain import EventLiveStream, EventVoDReady, EventEndpointFailed, \
    EventPublishTimeoutError, EventEncoderNotOpenedError

from apps import app, db
from apps.antmedia.domain import CustomerWebhookLiveStreamStarted, CustomerWebhookLiveStreamEnd, StreamAuthResp, \
    S3AgentEvent
from apps.date_utils import get_timestamp, sub_2date, datetime_to_str
from apps.models import LiveStream, Application, StreamingHistory, S3Storage, Vod, EventLog
from apps.utils import get_random_string, telegram_bot_sendtext


def send_notification(message):
    try:
        telegram_bot_sendtext(bot_message=message,
                              tele_url=app.config['TELEGRAM_BOT_CHAT_API_URL'],
                              token=app.config['TELEGRAM_BOT_TOKEN'],
                              chat_id=app.config['TELEGRAM_BOT_CHATID'],
                              tag=app.config['TELEGRAM_TAG'],
                              )
    except Exception as e:
        app.logger.error(e)


class EndpointManager:

    @staticmethod
    def format_data(event, start_time=None, end_time=None):
        action = event.action
        if action == 'liveStreamStarted':
            return CustomerWebhookLiveStreamStarted(
                stream_id=event.id,
                action=action,
                start_time=start_time
            )
        if action == 'liveStreamEnded':
            return CustomerWebhookLiveStreamEnd(
                stream_id=event.id,
                action=action,
                start_time=start_time,
                end_time=end_time
            )

    @retry(tries=3, delay=1)
    def send_event_to_customer(self, url: str, event, start_time=None, end_time=None):
        resp = False
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = self.format_data(event, start_time, end_time)
        r = requests.post(url, data=data.to_json(), headers=headers, timeout=2, verify=False)
        if r.status_code == 200:
            resp = True
        return resp

    @retry(tries=3, delay=1)
    def send_event_to_s3_agent(self, url: str, data: S3AgentEvent):
        resp = False
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data=data.to_json(), headers=headers, timeout=2, verify=False)
        if r.status_code == 200:
            resp = True
        return resp


class EventManager:

    def format_s3_path(self):
        pass

    @staticmethod
    def handle_livestream_started(event: EventLiveStream) -> str:
        """Ant Media server calls this hook when a new live stream is started."""
        try:

            stream_id = event.id
            livestream = LiveStream.query.filter_by(stream_id=stream_id, deleted=0). \
                order_by(LiveStream.id.desc()).first()
            if not livestream:
                return f'handle_livestream_started: stream not found with event.id={event.id}'

            app_id = livestream.application.id
            antmedia_app = Application.query.filter_by(id=app_id, deleted=0).order_by(Application.id.desc()).first()
            if not antmedia_app:
                return f'handle_livestream_started: app not found with event.id={event.id}'

            # 1. Update Livestream status
            time_now = get_timestamp()
            livestream.streaming_status = 1  # broadcasting
            livestream.event_start_on = time_now
            livestream.changed_on = time_now
            db.session.commit()
            # 2. Check session id
            stream_history = StreamingHistory.query.filter_by(livestream_id=livestream.id). \
                order_by(StreamingHistory.id.desc()).first()
            if not stream_history:
                return f'handle_livestream_ended: stream_history with livestream.id {livestream.id} not found'
            session_id = stream_history.session_id
            # 3. Fire event to Customer Endpoint if customer enable this feature
            if antmedia_app.webhook_url:
                start_time = datetime_to_str(time_now)
                send = False
                try:
                    send = EndpointManager().send_event_to_customer(antmedia_app.webhook_url, event, start_time)
                except Exception as e:
                    app.logger.error(e)
                if not send:
                    msg = f'handle_livestream_started: send to {antmedia_app.webhook_url} failed. ' \
                          f'stream_id: {stream_id}, session_id: {session_id}'
                    send_notification(msg)
            # 4. Fire event to S3 Upload Agent if customer enable this feature
            if antmedia_app.s3_enable:
                app.logger.info("Push event to S3 upload agent")
                """Get S3 Info"""
                s3_storage_id = antmedia_app.s3_storage_id
                s3 = S3Storage.query.filter_by(id=s3_storage_id).order_by(S3Storage.id.desc()).first()
                if not s3:
                    msg = f's3 not found with event.id={event.id}'
                    app.logger.error(msg)
                    send_notification(msg)
                else:
                    s3_agent_event = S3AgentEvent(stream_id=stream_id,
                                                  app_name=antmedia_app.name,
                                                  s3_endpoint=s3.s3_endpoint,
                                                  s3_bucket=s3.s3_bucket,
                                                  s3_access_key=s3.s3_access_key,
                                                  s3_secret_key=s3.s3_secret_key,
                                                  s3_enable_tls=s3.s3_enable_tls)
                    s3_agent_endpoints = app.config['S3_AGENT_ENDPOINTS']
                    for url in s3_agent_endpoints:
                        send = False
                        try:
                            send = EndpointManager().send_event_to_s3_agent(url, s3_agent_event)
                        except Exception as e:
                            app.logger.error(e)
                        if not send:
                            msg = f'handle_livestream_started: send to s3 agent: url failed. ' \
                                  f'stream_id: {stream_id}, session_id: {session_id}, event: {s3_agent_event.to_json()}'
                            send_notification(msg)
        except Exception as e:
            app.logger.error(e)
            msg = f'handle_livestream_started: error occurred. \n' \
                  f'stream_id: {event.id}. \n' \
                  f'exception: {str(e)}'
            return msg

    @staticmethod
    def handle_livestream_ended(event: EventLiveStream):
        """Ant Media Server calls this hook when a live stream is ended."""
        try:
            stream_id = event.id
            livestream = LiveStream.query.filter_by(stream_id=stream_id, deleted=0). \
                order_by(LiveStream.id.desc()).first()
            if not livestream:
                return f'handle_livestream_ended: stream not found with event.id={event.id}'

            app_id = livestream.application.id
            antmedia_app = Application.query.filter_by(id=app_id, deleted=0).order_by(Application.id.desc()).first()
            if not antmedia_app:
                return f'handle_livestream_ended: app not found with event.id={event.id}'

            # 1. Update LiveStream status
            time_now = get_timestamp()
            event_start_on = livestream.event_start_on
            time_now_str = datetime_to_str(time_now)
            duration = sub_2date(time_now_str, event_start_on)
            livestream.event_finish_on = time_now
            livestream.duration = duration
            livestream.changed_on = time_now
            livestream.streaming_status = 0  # offline
            db.session.commit()

            # 2. Update stream history
            # stream_history = StreamingHistory.query.filter_by(livestream_id=livestream.id). \
            #     order_by(StreamingHistory.id.desc()).first()
            # if not stream_history:
            #     return f'handle_livestream_ended: stream_history with livestream.id {livestream.id} not found'
            # stream_history.end_time = time_now
            # stream_history.changed_on = time_now
            # stream_history.completed = 1
            # db.session.commit()

            SessionStreamManager().update_session_history(stream_id=stream_id, status=8, end_time=True)

            # 3. Fire event to Customer Endpoint if customer enable this feature.
            webhook_url = antmedia_app.webhook_url
            if webhook_url:
                app.logger.info('send event to endpoint')
                start_time = event_start_on
                end_time = time_now
                send = False
                try:
                    send = EndpointManager().send_event_to_customer(webhook_url, event, start_time, end_time)
                except Exception as e:
                    app.logger.error(e)
                if not send:
                    msg = f'handle_livestream_ended: send to {antmedia_app.webhook_url} failed. \n' \
                          f'stream_id: {stream_id}'
                    send_notification(msg)
        except Exception as e:
            msg = f'handle_livestream_ended: error occurred. \n' \
                  f'stream_id: {event.id}. \n' \
                  f'exception: {str(e)}'
            return msg

    @staticmethod
    def handle_vod_ready(event: EventVoDReady):
        """Ant Media Server calls this hook when the recording of the live stream is ended."""
        try:
            stream_id = event.id
            livestream = LiveStream.query.filter_by(stream_id=stream_id, deleted=0). \
                order_by(LiveStream.id.desc()).first()
            if not livestream:
                return f'handle_vod_ready: stream not found with event.id={event.id}'

            app_id = livestream.application.id
            antmedia_app = Application.query.filter_by(id=app_id, deleted=0).order_by(Application.id.desc()).first()
            if not antmedia_app:
                return f'handle_vod_ready: app not found with event.id={event.id}'

            """Get S3 Info"""
            s3_storage_id = antmedia_app.s3_storage_id
            s3 = S3Storage.query.filter_by(id=s3_storage_id).order_by(S3Storage.id.desc()).first()
            if not s3:
                return False, f's3 not found with event.id={event.id}'

            """Update vod record"""
            antmedia_vod_id = event.vodId
            vod_name = event.vodName
            stream_history = StreamingHistory.query.filter_by(livestream_id=livestream.id). \
                order_by(StreamingHistory.id.desc()).first()
            if not stream_history:
                return f'handle_vod_ready: stream_history with livestream.id {livestream.id} not found'

            session_id = stream_history.session_id
            start_time = stream_history.start_time
            # Create new vod record
            time_now = get_timestamp()
            s3_link = f'https://{s3.s3_endpoint}/{s3.s3_bucket}/{antmedia_vod_id}_{vod_name}'
            hls_link = ''
            vod = Vod(
                livestream_id=livestream.id,
                antmedia_vod_id=antmedia_vod_id,
                session_id=session_id,
                s3_link=s3_link,
                hls_link=hls_link,
                start_time=start_time,
                end_time=time_now,
                created_on=time_now
            )
            db.session.add(vod)
            db.session.commit()
            db.session.refresh(vod)
            vod_id = vod.id
            stream_history = StreamingHistory.query.filter_by(livestream_id=livestream.id). \
                order_by(StreamingHistory.id.desc()).first()
            stream_history.vod_id = vod_id
            db.session.commit()
        except Exception as e:
            msg = f'handle_vod_ready: error occurred \n ' \
                  f'stream_id: {event.id} \n ' \
                  f'exception: {str(e)}'
            return msg

    def handle_endpoint_failed(self, event: EventEndpointFailed):
        """Ant Media server calls this hook when the RTMP endpoint broadcast went into the failed status."""
        pass

    def handle_publish_timeout_error(self, event: EventPublishTimeoutError):
        """Ant Media server calls this hook when there is a publish time out error,
        it generally means that the server is not getting any frames."""
        pass

    def handle_encoder_not_opened_error(self, event: EventEncoderNotOpenedError):
        """Ant Media server calls this hook when the encoder can't be opened."""
        pass

    def handle_vod_upload_callback(self, event):

        # Update vod record

        # Fire event to Customer Endpoint if customer enable this feature.
        pass

    @staticmethod
    def insert_event_log(event, worker_queue):
        try:
            stream_id = event.id
            action = event.action
            status = 8
            time_now = get_timestamp()
            event_log = EventLog(
                stream_id=stream_id,
                action=action,
                status=status,
                event=event.to_dict(),
                worker_queue=worker_queue,
                created_on=time_now)
            db.session.add(event_log)
            db.session.commit()
            db.session.refresh(event_log)
            return True, event_log.id
        except Exception as e:
            app.logger.error(e)
            return False, "error occurred"

    @staticmethod
    def update_event_log(event_log_id, status, reason_error=None):
        try:
            event_log = EventLog.query.filter_by(id=event_log_id).order_by(EventLog.id.desc()).first()
            if not event_log:
                return "event_log record not found with id: {}".format(event_log_id)
            event_log.status = status
            if reason_error:
                event_log.reason_error = reason_error
            time_now = get_timestamp()
            event_log.changed_on = time_now
            db.session.commit()
        except Exception as e:
            app.logger.error(e)
            return "error occurred"

    @staticmethod
    def check_duplicate_event(event):
        """Check duplicate event"""
        try:
            action = event.action
            stream_id = event.id
            event_log = EventLog.query.filter_by(stream_id=stream_id).order_by(EventLog.id.desc()).first()
            if event_log and action == event_log.action:
                time_now = get_timestamp()
                event_log = EventLog(
                    stream_id=stream_id,
                    action=action,
                    status=-1,
                    event=event.to_dict(),
                    reason_error='duplicate event',
                    created_on=time_now)
                db.session.add(event_log)
                db.session.commit()
                return True
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def count_event_log_records(status):
        try:
            return EventLog.query.filter_by(status=status).count()
        except Exception as e:
            app.logger.error(e)

    @staticmethod
    def check_livestream_started_finished(event):
        try:
            action = 'liveStreamStarted'
            stream_id = event.id
            event_log = EventLog.query.filter_by(stream_id=stream_id, action=action). \
                order_by(EventLog.id.desc()).first()
            if event_log and event_log.status == 8:
                time_now = get_timestamp()
                event_log = EventLog(
                    stream_id=stream_id,
                    action=action,
                    status=-1,
                    event=event.to_dict(),
                    reason_error=f'liveStreamStarted of stream_id: {stream_id} not finish',
                    created_on=time_now)
                db.session.add(event_log)
                db.session.commit()
                return False
        except Exception as e:
            app.logger.error(e)
            return False
        return True


class StreamAuthentication:

    @staticmethod
    def verify_link_livestream(stream_id: str, token: str, action=None) -> (bool, StreamAuthResp):
        """Verify livestream link that client push to and init the new session history"""
        try:
            livestream = LiveStream.query.filter_by(stream_id=stream_id, publish_token=token, deleted=0).first()
            if not livestream:
                return False, StreamAuthResp(error=f'livestream not found with stream_id: {stream_id}, '
                                                   f'token: {token}')

            app_id = livestream.application.id
            antmedia_app = Application.query.filter_by(id=app_id, deleted=0).order_by(Application.id.desc()).first()
            if not antmedia_app:
                return False, StreamAuthResp(error='app name not found')
            if action == 'liveStreamStarted':
                antmedia_app_name = antmedia_app.name
                current_session = StreamingHistory.query.join(LiveStream, StreamingHistory.livestream_id == LiveStream.id). \
                    filter(LiveStream.stream_id == stream_id).order_by(StreamingHistory.id.desc()).first()

                if not current_session or current_session.completed == 1:
                    ok, data = SessionStreamManager().init_session_history(livestream_id=livestream.id)
                    if not ok:
                        return False, StreamAuthResp(error=data)
                    return True, StreamAuthResp(session_id=data, app_name=antmedia_app_name)

                if current_session and current_session.completed != 1:
                    return False, StreamAuthResp(error=f'stream_id: {stream_id}. session current not finish')

            return True, StreamAuthResp(error='None')
        except Exception as e:
            app.logger.error(e)
            return False, StreamAuthResp(error=str(e))


class SessionStreamManager:

    @staticmethod
    def init_session_history(livestream_id: str) -> (bool, str):
        """Initial session history record"""
        try:
            time_now = get_timestamp()
            db.session.commit()
            session_id = get_random_string()
            stream_ss = StreamingHistory(
                livestream_id=livestream_id,
                start_time=time_now,
                session_id=session_id,
                created_on=time_now,
                completed=0
            )
            db.session.add(stream_ss)
            db.session.commit()
            return True, session_id
        except Exception as e:
            app.logger.error(e)
            return False, str(e)

    @staticmethod
    def get_session_id_current(stream_id: str) -> (bool, str):
        try:
            record = StreamingHistory.query.join(LiveStream, StreamingHistory.livestream_id == LiveStream.id). \
                filter(LiveStream.stream_id == stream_id).order_by(StreamingHistory.id.desc()).first()
            if record:
                return True, record.session_id
            return False, f'session id not found with stream {stream_id}'
        except Exception as e:
            app.logger.error(e)
            return False, str(e)

    @staticmethod
    def update_session_history(stream_id: str, status: int, end_time: bool):
        try:
            # stream_history = StreamingHistory.query.filter_by(livestream_id=livestream_id). \
            #     order_by(StreamingHistory.id.desc()).first()
            stream_history = StreamingHistory.query.join(LiveStream, StreamingHistory.livestream_id == LiveStream.id). \
                filter(LiveStream.stream_id == stream_id).order_by(StreamingHistory.id.desc()).first()
            if not stream_history:
                return False, f'update_session_history: stream_history with stream id {stream_id} not found'
            time_now = get_timestamp()
            if end_time:
                stream_history.end_time = time_now
            stream_history.changed_on = time_now
            stream_history.completed = status
            db.session.commit()
            return True, 'success'
        except Exception as e:
            app.logger.error(e)
            return False, str(e)


class S3Manager:

    @staticmethod
    def get_s3_info(stream_id):
        livestream = LiveStream.query.filter_by(stream_id=stream_id, deleted=0). \
            order_by(LiveStream.id.desc()).first()
        if not livestream:
            return f'get_s3_info: stream not found with stream_id: {stream_id}'

        app_id = livestream.application.id
        antmedia_app = Application.query.filter_by(id=app_id, deleted=0).order_by(Application.id.desc()).first()
        if not antmedia_app:
            return f'get_s3_info: app not found with stream_id: {stream_id}'

        """Get S3 Info"""
        s3_storage_id = antmedia_app.s3_storage_id
        s3 = S3Storage.query.filter_by(id=s3_storage_id).order_by(S3Storage.id.desc()).first()
        if not s3:
            return False, f'get_s3_info: s3 not found with stream_id: {stream_id}'
        return True, s3.to_json()
