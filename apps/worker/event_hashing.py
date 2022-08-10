import time

from uhashring import HashRing
from apps.worker.tasks import event_handle_worker_1, event_handle_worker_2, worker_1, worker_2
from apps.antmedia.domain import EventLiveStream

# create a consistent hash ring of 2 nodes of weight 1
hr = HashRing(nodes=['event_handle_worker_1', 'event_handle_worker_2'])

hr1 = HashRing(nodes=['worker_1', 'worker_2'])

dispatcher = {
    'worker_1': worker_1.delay,
    'worker_2': worker_2.delay,

    'event_handle_worker_1': event_handle_worker_1.delay,
    'event_handle_worker_2': event_handle_worker_2.delay
}


def call_func(x, y, func):
    try:
        my_func = dispatcher[func]
        return my_func(x, y)
    except:
        return "Invalid function"


def call_func_event(e, func):
    try:
        my_func = dispatcher[func]
        print(my_func)
        return my_func(e)
    except:
        return "Invalid function"






# for i in range(10):
#     time.sleep(1)
#     w = hr1.get_node(str(i))
#     print(w)
#     call_func(2, 3, w)


# add.delay(2, 3)

event = EventLiveStream(id="uhtcvzgjpyjbktpqrhouzgjywwymiojp", action="liveStreamStarted")
worker = hr.get_node(event.id)
print(worker)
call_func_event(event.to_dict(), worker)
#
# handle_event_worker(event)