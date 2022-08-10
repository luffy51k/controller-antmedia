# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present EVG
"""
import json
import time
from urllib import parse

import redis
from antmedia_client.base import AntmediaClient
from flask import jsonify, make_response, request
from uhashring import HashRing

from apps import app
from apps.antmedia.core import StreamAuthentication, EventManager, send_notification, SessionStreamManager, S3Manager
from apps.worker.tasks import event_handle_worker_1, event_handle_worker_2, worker_1, worker_2, event_handle_worker_3, \
    event_handle_worker_4, event_handle_worker_5
from apps.worker.tasks import my_task
from . import blueprint
from .domain import StreamRequestCreate, AppSettings, Stream, EventLiveStream
from .validater import (
    validate_app_settings_params,
    validate_create_app_req,
    validate_stream_bulk_req,
    validate_stream_req,
    validate_event_req, validate_stream_authenticate_req, validate_stream_history_completed_req
)
# create a consistent hash ring of 2 nodes of weight 1
from ..auth.core import api_login_required
from ..date_utils import format_timestamp_to_str_time

hr = HashRing(nodes=app.config['CELERY_EVENT_WORKERS'])

dispatcher = {
    'worker_1': worker_1.delay,
    'worker_2': worker_2.delay,
    'event_handle_worker_1': event_handle_worker_1.delay,
    'event_handle_worker_2': event_handle_worker_2.delay,
    'event_handle_worker_3': event_handle_worker_3.delay,
    'event_handle_worker_4': event_handle_worker_4.delay,
    'event_handle_worker_5': event_handle_worker_5.delay
}
client = AntmediaClient(
    antmedia_uri=app.config.get("ANTMEDIA_URI"),
    antmedia_user=app.config.get("ANTMEDIA_USER"),
    antmedia_password=app.config.get("ANTMEDIA_PASSWORD")
)


@blueprint.route("/", methods=["GET"])
@api_login_required
def index():
    my_task.delay()
    return make_response(jsonify({"msg": "ok"}))


@blueprint.route("/auth", methods=["GET"])
def api_wss_auth():
    try:
        app.logger.debug(f'Request header: {request.headers}')
        x_original_uri = request.headers['X-Original-URI']
        app.logger.debug(f'Header X-Original-URI: {x_original_uri}')
        if x_original_uri is None:
            msg = 'api_wss_auth: X-Original-URI header is missing'
            send_notification(msg)
            return make_response(msg, 400)

        params = parse.urlsplit(x_original_uri).query
        params = params.split('&')
        # Validate stream_name param
        stream_param = params[0].split('=')
        if 'stream_name' not in stream_param:
            msg = 'api_wss_auth: stream_name param is in-validate'
            send_notification(msg)
            return make_response(msg, 400)
        if stream_param[1] is None or len(stream_param[1]) == 0:
            msg = 'api_wss_auth: stream_name param is empty'
            send_notification(msg)
            return make_response(msg, 400)
        stream_id = stream_param[1]

        # Validate token param
        token_param = params[1].split('=')
        if 'token' not in token_param:
            msg = 'api_wss_auth: token param is in-validate'
            return make_response(msg, 400)
        if token_param[1] is None or len(token_param[1]) == 0:
            msg = 'api_wss_auth: token param is empty'
            return make_response(msg, 400)
        token = token_param[1]

        verified, data = StreamAuthentication().verify_link_livestream(stream_id, token, action=None)
        if not verified:
            msg = f'api_wss_auth: authentication failed. stream_id: {stream_id}, token: {token}. Resp: {data.to_json()}'
            app.logger.warning(msg)
            send_notification(msg)
            return make_response(msg, 401)

        # success
        return make_response('1', 200)

    except Exception as e:
        app.logger.error(e)
        resp = {
            "success": False,
            "data": "api_wss_auth: code error happened."
        }
        return make_response(jsonify(resp), 410)


@blueprint.route("/api/v1/app/authenticate", methods=["POST"])
@api_login_required
def api_app_authenticate():
    app.logger.info(request.form)
    app.logger.info(request.json)
    validated, req = validate_stream_authenticate_req(request.json)
    if not validated:
        return make_response(req, 400)
    token = filter_stream_token_val(req['queryParams'])
    stream_id = req['name']
    verified, data = StreamAuthentication().verify_link_livestream(stream_id, token)
    if not verified:
        msg = f'authentication failed. stream_id: {stream_id}, token: {token}. Resp: {data.to_json()}'
        app.logger.warning(msg)
        return make_response(msg, 401)
    return make_response(jsonify({"msg": "ok"}))


@blueprint.route("/status", methods=["GET"])
@api_login_required
def status():
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
    total_event_process_error = EventManager().count_event_log_records(status=-1) + EventManager(). \
        count_event_log_records(status=-2)
    metrics = {
        'total_event_process_error': total_event_process_error,
        'redis_event_handle_worker_1': redis_client.llen('event_handle_worker_1'),
        'redis_event_handle_worker_2': redis_client.llen('event_handle_worker_2'),
        'redis_event_handle_worker_3': redis_client.llen('event_handle_worker_3'),
        'redis_event_handle_worker_4': redis_client.llen('event_handle_worker_4'),
        'redis_event_handle_worker_5': redis_client.llen('event_handle_worker_5'),
    }
    return make_response(jsonify(metrics))


@blueprint.route("/api/v1/app/<app_name>/streams", methods=["GET"])
@api_login_required
def api_list_streams(app_name):
    success, data = client.stream.list_streams(app_name)
    if not success:
        resp = {"success": False, "data": data}
    else:
        resp = {"success": True, "data": data}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/<app_name>/stream/<stream_id>", methods=["GET"])
@api_login_required
def api_stream(app_name, stream_id):
    if request.method == "GET":
        success, data = client.stream.get_stream(app_name, stream_id)
        if not success:
            resp = {"success": False, "data": data}
        else:
            resp = {"success": True, "data": data}

        return make_response(jsonify(resp))
    if request.method == "POST":
        client.stream.update_stream()


@blueprint.route("/api/v1/app/<app_name>/stream/<stream_id>/stop", methods=["POST"])
@api_login_required
def api_stop_stream(app_name, stream_id):
    data = client.stream.stop_stream(app_name, stream_id)
    print(data)
    if data is not None:
        resp = {"success": False, "data": data}
    else:
        resp = {"success": True, "data": "stop stream success"}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/<app_name>/stream/<stream_id>/start", methods=["POST"])
@api_login_required
def api_start_stream(app_name, stream_id):
    data = client.stream.start_stream(app_name, stream_id)
    if data is not None:
        resp = {"success": False, "data": data}
    else:
        resp = {"success": True, "data": "start stream success"}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/<app_name>/stream/create", methods=["POST"])
@api_login_required
def api_create_stream(app_name):
    validated, req = validate_stream_req(request.json)
    if not validated:
        return make_response(req, 400)
    req = StreamRequestCreate(**req)
    data = client.stream.create_stream(app_name, req)
    print(data)
    if data is not None:
        resp = {"success": False, "data": "can not create stream"}
    else:
        resp = {"success": True, "data": "create stream success"}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/<app_name>/stream/bulk", methods=["DELETE"])
@api_login_required
def api_delete_bulk_streams(app_name):
    validated, req = validate_stream_bulk_req(request.json)
    if not validated:
        return make_response(req, 400)
    streams = req["streams"]
    data = client.stream.delete_bulk_streams(app_name, streams)
    print(data)
    if data is not None:
        resp = {"success": False, "data": "can not delete bulk stream"}
    else:
        resp = {"success": True, "data": "delete bulk stream success"}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/<app_name>/stream/<stream_id>", methods=["DELETE"])
@api_login_required
def api_delete_stream(app_name, stream_id):
    data = client.stream.delete_stream(app_name, stream_id)
    print(data)
    if data is not None:
        resp = {"success": False, "data": "can not delete stream"}
    else:
        resp = {"success": True, "data": "delete stream success"}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/create", methods=["POST"])
@api_login_required
def api_create_app():
    validated, req = validate_create_app_req(request.json)
    if not validated:
        return make_response(req, 400)

    app_name = req["name"]
    data = client.app.create_app(app_name)
    print(data)
    if data is not None:
        resp = {"success": False, "data": data}
    else:
        resp = {"success": True, "data": "create app success"}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/<app_name>", methods=["DELETE"])
@api_login_required
def api_delete_app(app_name):
    data = client.app.delete_app(app_name)
    print(data)
    if data is not None:
        resp = {"success": False, "data": data}
    else:
        resp = {"success": True, "data": "delete app success"}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/lists", methods=["GET"])
@api_login_required
def api_list_apps():
    success, data = client.app.get_apps()
    if not success:
        resp = {"success": False, "data": data}
    else:
        resp = {"success": True, "data": data}

    return make_response(jsonify(resp))


@blueprint.route("/api/v1/app/<app_name>/settings", methods=["GET", "PUT"])
@api_login_required
def api_get_app_settings(app_name):
    if request.method == "GET":
        success, data = client.app.get_app_settings(app_name)
        if not success:
            resp = {"success": False, "data": data}
        else:
            resp = {"success": True, "data": data}

        return make_response(jsonify(resp))

    if request.method == "PUT":
        validated, req = validate_app_settings_params(request.json)
        if not validated:
            return make_response(req, 400)
        req = AppSettings(**req)
        resp = client.app.update_app_settings(app_name, req)
        if resp is not None:
            resp = {"success": False, "data": resp}
        else:
            resp = {"success": True, "data": "Update app settings success"}

        return make_response(jsonify(resp))


"""HANDLE STREAM EVENTS"""


@blueprint.route("/api/v1/webhook-stream-event", methods=["POST"])
@api_login_required
def api_handle_stream_event():
    try:
        app.logger.info(request.form)
        validated, event = validate_event_req(request.form)
        app.logger.info(validated)
        app.logger.info(event)
        if not validated:
            return make_response(event, 400)

        save_event_to_file(event)
        """Check duplicate event"""
        duplicated = EventManager().check_duplicate_event(event)
        if duplicated:
            resp = {"success": False, "data": f"event duplicated. stream_id: {event.id}"}
            send_notification(resp['data'])
            return make_response(jsonify(resp))
        """Check Event liveStreamStarted must finished"""
        finished = EventManager().check_livestream_started_finished(event)
        if not finished:
            resp = {"success": False, "data": f"Event liveStreamStarted of stream id: {event.id} not finish"}
            send_notification(resp['data'])
            return make_response(jsonify(resp))
        worker = hr.get_node(event.id)
        ok, data = EventManager().insert_event_log(event, worker)
        if not ok:
            resp = {"success": False, "data": data}
            return make_response(jsonify(resp))
        call_func_event(event=event.to_dict(), event_log_id=data, func=worker)
    except Exception as e:
        app.logger.error(e)

    resp = {"success": True, "data": "receive event success"}
    return make_response(jsonify(resp))


@blueprint.route("/api/v1/stream-history/completed", methods=["GET"])
def api_stream_history_completed():
    app.logger.info(request.args)
    # Validate request params
    stream_id = request.args.get('stream_id')
    if not stream_id:
        return make_response('missing stream_id param', 400)
    completed = request.args.get('completed')
    if not completed:
        return make_response('missing completed param', 400)
    ok, data = SessionStreamManager().update_session_history(stream_id, int(completed), False)
    if not ok:
        resp = {
            "success": False,
            "data": "Code error happened with sql"
        }
        return make_response(jsonify(resp), 410)
    resp = {
        "success": True,
        "data": "Update data success"
    }
    return make_response(jsonify(resp), 200)


@blueprint.route("/api/v1/stream/session-current", methods=["GET"])
def api_get_stream_session_current():
    try:
        app.logger.info(request.args)
        # Validate request params
        stream_id = request.args.get('stream_id')
        if not stream_id:
            return make_response('missing stream_id param', 400)
        ok, session_id = SessionStreamManager().get_session_id_current(stream_id)
        if not ok:
            resp = {"success": False,
                    "data": f"api_get_stream_session_current: session_id can not found. stream_id: {stream_id}"}
            send_notification(resp['data'])
            return make_response(jsonify(resp))

        ok, s3 = S3Manager().get_s3_info(stream_id)
        if not ok:
            resp = {"success": False,
                    "data": f"api_get_stream_session_current: s3 can not found. stream_id: {stream_id}"}
            send_notification(resp['data'])
            return make_response(jsonify(resp))

        resp = {
            "success": True,
            "session_id": session_id,
            "s3_url": s3['s3_endpoint'],
            "s3_access_key": s3['s3_access_key'],
            "s3_secret_key": s3['s3_secret_key'],
            "bucket": s3['s3_bucket']
        }
        return make_response(jsonify(resp))
    except Exception as e:
        app.logger.error(e)
        resp = {
            "success": False,
            "data": "Code error happened."
        }
        return make_response(jsonify(resp), 410)


@blueprint.route("/api/v1/rtmpgw-receiver", methods=["GET"])
def api_handle_rtmpgw_receiver():

    app.logger.info(request.args)
    # Validate request params
    token = request.args.get('token')
    if not token:
        msg = 'api_handle_rtmpgw_receiver: missing token param'
        send_notification(msg)
        return make_response(msg, 400)
    action = request.args.get('action')
    if not action:
        msg = 'api_handle_rtmpgw_receiver: missing action param'
        send_notification(msg)
        return make_response(msg, 400)
    stream_id = request.args.get('stream_id')
    if not stream_id:
        msg = 'api_handle_rtmpgw_receiver: missing stream_id param'
        send_notification(msg)
        return make_response(msg, 400)

    event = EventLiveStream(action=action, id=stream_id)

    # store event to file. Help you trace events.
    save_event_to_file(event)

    # Check authentication
    verified, data = StreamAuthentication().verify_link_livestream(stream_id, token, action)
    if not verified:
        msg = f'authentication failed. stream_id: {stream_id}, token: {token}. Resp: {data.to_json()}'
        send_notification(msg)
        app.logger.warning(msg)
        return make_response(msg, 401)

    # Check duplicate event
    duplicated = EventManager().check_duplicate_event(event)
    if duplicated:
        resp = {"success": False, "data": f"event duplicated. stream_id: {event.id}"}
        send_notification(resp['data'])
        return make_response(jsonify(resp))

    # Check Event liveStreamStarted must finish
    finished = EventManager().check_livestream_started_finished(event)
    if not finished:
        resp = {"success": False, "data": f"Event liveStreamStarted of stream id: {event.id} not finish."
                                          f"May be Celery worker is not working."}
        send_notification(resp['data'])
        return make_response(jsonify(resp))

    # Insert to event_log table
    worker = hr.get_node(event.id)
    ok, data = EventManager().insert_event_log(event, worker)
    if not ok:
        resp = {"success": False, "data": f"insert event log error: {data}"}
        send_notification(resp['data'])
        return make_response('0', 200)

    # Push to Celery Worker
    call_func_event(event=event.to_dict(), event_log_id=data, func=worker)

    return make_response('1', 200)


def call_func_event(event, event_log_id, func):
    try:
        my_func = dispatcher[func]
        print(my_func)
        return my_func(event, event_log_id)
    except:
        return "Invalid function"


def save_event_to_file(event):
    data = {
        'remote_addr': request.remote_addr,
        'datetime': format_timestamp_to_str_time(),
        'stream_id': event.id,
        'action': event.action,
        'event': event.to_dict()
    }

    with open("logs/stream_events.txt", "a") as outfile:
        outfile.write(json.dumps(data))
        outfile.write('\n')


def filter_stream_token_val(token: str):
    token = token.split('=')
    return token[1].replace('}', '')
