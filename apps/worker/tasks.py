from apps import celery_app, app
import random
from celery.utils.log import get_task_logger

from apps.antmedia.core import EventManager, send_notification
from apps.date_utils import get_timestamp, datetime_to_str, sub_2date
from apps.models import LiveStream, Application, EventLog
from apps.antmedia.domain import EventLiveStream, EventVoDReady, EventEndpointFailed, \
    EventPublishTimeoutError, EventEncoderNotOpenedError

logger = get_task_logger(__name__)
celery = celery_app


def handle_event(event, event_log_id):
    logger.debug(f'Begin handle event: {event}')
    error = None
    action = event['action']
    if action == 'liveStreamStarted':
        error = EventManager().handle_livestream_started(EventLiveStream(**event))
    elif action == 'liveStreamEnded':
        error = EventManager().handle_livestream_ended(EventLiveStream(**event))
    elif action == 'vodReady':
        error = EventManager().handle_vod_ready(EventVoDReady(**event))
    elif action == 'endpointFailed':
        error = EventManager().handle_endpoint_failed(EventEndpointFailed(**event))
    elif action == 'publishTimeoutError':
        error = EventManager().handle_publish_timeout_error(EventPublishTimeoutError(**event))
    elif action == 'encoderNotOpenedError':
        error = EventManager().handle_encoder_not_opened_error(EventEncoderNotOpenedError(**event))
    else:
        logger.error("Event: action not allow")
        error = "Event: action not allow"
    # Update event_log status
    status = 1
    if error:
        logger.error(error)
        status = -1
        send_notification(str(error))
    EventManager().update_event_log(event_log_id, status, reason_error=error)


@celery.task()
def event_handle_worker_1(event: dict, event_log_id):
    handle_event(event, event_log_id)


@celery.task()
def event_handle_worker_2(event: dict, event_log_id):
    handle_event(event, event_log_id)


@celery.task()
def event_handle_worker_3(event: dict, event_log_id):
    handle_event(event, event_log_id)


@celery.task()
def event_handle_worker_4(event: dict, event_log_id):
    handle_event(event, event_log_id)


@celery.task()
def event_handle_worker_5(event: dict, event_log_id):
    handle_event(event, event_log_id)


@celery.task()
def add(x, y):
    result = x + y
    logger.debug(f'Add: {x} + {y} = {result}')
    return result


@celery.task()
def worker_1(x, y):
    result = x + y
    logger.debug(f' Worker_1 Add: {x} + {y} = {result}')
    return result


@celery.task()
def worker_2(x, y):
    result = x + y
    logger.debug(f' Worker_2 Add: {x} + {y} = {result}')
    return result


@celery.task()
def worker_3(x, y):
    result = x + y
    logger.debug(f' Worker_3 Add: {x} + {y} = {result}')
    return result


@celery.task()
def worker_4(x, y):
    result = x + y
    logger.debug(f' Worker_4 Add: {x} + {y} = {result}')
    return result


@celery.task()
def worker_5(x, y):
    result = x + y
    logger.debug(f' Worker_5 Add: {x} + {y} = {result}')
    return result


@celery.task(bind=True)
def my_task(self):
    choice = random.choice(['Alpha',
                            'Beta',
                            'Gamma',
                            'Delta',
                            'Epsilon',
                            'Zeta',
                            'Eta',
                            'Theta',
                            'Iota',
                            'Kappa',
                            'Lambda',
                            'Mu',
                            'Nu',
                            'Xi',
                            'Omicron',
                            'Pi',
                            'Rho',
                            'Sigma',
                            'Tau',
                            'Upsilon',
                            'Phi',
                            'Chi',
                            'Psi',
                            'Omega'])

    return choice


@celery.task(name="periodic_task")
def periodic_task():
    app.logger.info('Hi! from periodic_task')
    livestreams = LiveStream.query.filter_by(deleted=0)
    for livestream in livestreams:
        app.logger.info(livestream)


@celery.task(name="periodic_app_task")
def periodic_app_task():
    app.logger.info('Hi! from periodic_task')
    application = Application.query.filter_by(deleted=0)
    for antmedia_app in application:
        app.logger.info(type(antmedia_app.app_setting))


@celery.task(name="periodic_event_log_task")
def periodic_event_log_task():
    app.logger.info('Hi! from periodic_event_log_task')
    events = EventLog.query.filter_by(status=8).all()
    time_now = datetime_to_str(get_timestamp())
    for event in events:
        created_on = event.created_on
        duration = sub_2date(time_now, created_on)
        if duration > 60:
            app.logger.error(f'event {event.stream_id} overtime to process')
            EventManager().update_event_log(event.id, -2, 'system error')
