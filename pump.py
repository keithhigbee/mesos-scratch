import os, pyrax, boto, uuid, time

# AWS IAM sms-rax user
AWS_ID = os.environ['AWS_ID']
AWS_SECRET = os.environ['AWS_SECRET']
TOPIC_ARN = os.environ['TOPIC_ARN']

# RAX account info
pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region('IAD')
pyrax.set_credentials(os.environ['RAX_ID'], os.environ['RAX_KEY'])

#assign generated client ID (see authentication section)
MY_CLIENT_ID = str(uuid.uuid4())

def main():
	# Connect to AWS SNS
	sns = boto.connect_sns(AWS_ID, AWS_SECRET)

	# Connect to RAX Cloud Queues
	pyrax.queues.client_id = MY_CLIENT_ID
	queue = pyrax.queues.get("sample_queue")	
	claim = queue.claim_messages(ttl=60, grace=120, count=25)

	while True:
		if claim != None:
			# Get messages off the RAX queue and pump to AWS topic
			for message in claim.messages:
				res = sns.publish(TOPIC_ARN, message.body)
				print message.body

				# remove from rax queue
				queue.delete_message(message.id, claim.id)
		else:
			time.sleep(10)

		# Get next set of mesasges off the queue
		claim = queue.claim_messages(ttl=60, grace=120, count=25)

main()