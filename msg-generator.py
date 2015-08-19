import pyrax, time, uuid

# RAX account info
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region('IAD')
pyrax.set_credentials('mesos.dev', 'eb87e9f28915423eb0c205e3b3d357e3')	

#assign generated client ID (see authentication section)
MY_CLIENT_ID = str(uuid.uuid4())

while True:
	# Connect to RAX Cloud Queues
	pyrax.queues.client_id = MY_CLIENT_ID
	queue = pyrax.queues.get("sample_queue")
	# msg_body = "Message body %s" % date.now().isoformat()
	msg_body = "Generated at: %s" % time.strftime("%c")
	queue.post_message(msg_body, ttl=300)
	print msg_body
	time.sleep(5)