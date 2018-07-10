import redis


r = redis.StrictRedis(host='leawood', port=6379, db=0)
pubsub = r.pubsub()
pubsub.subscribe(['test_channel','another_channel'])
for item in pubsub.listen():
	print("DATA: {}".format(item))


