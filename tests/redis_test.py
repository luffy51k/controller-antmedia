import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

print(redis_client.llen('event_handle_worker_1'))
print(redis_client.llen('event_handle_worker_2'))


import ansible_runner

r = ansible_runner.run()