from apps.antmedia.domain import EventLiveStream
from apps.worker.event_hashing import handle_event_worker

event = EventLiveStream(id="uhtcvzgjpyjbktpqrhouzgjywwymiojp", action="liveStreamStart")

handle_event_worker(event)