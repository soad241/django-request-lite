import logging

from carrot.connection import DjangoAMQPConnection
from carrot.messaging import Publisher, Consumer
from django.db import transaction
from gattlib.string_tools import convert_unicode_to_string

import models

logger = logging.getLogger('djangoproject.request.request_sync_requests')


def record_request(request):
    key = "request.request_hit"
    return _send_message(key, request)

def _send_message(routing_key, request):
    conn = DjangoAMQPConnection()
    publisher = Publisher(connection=conn, exchange='request', 
                          exchange_type='topic', routing_key=routing_key, 
                          serializer='pickle')
    publisher.send(request)
    publisher.close()
    conn.close()

@transaction.commit_on_success()
def save_hits():
    conn = DjangoAMQPConnection()
    consumer = Consumer(connection=conn, queue='requestrequesthitqueue', 
                        exchange='request', 
                        routing_key='request.*', exchange_type='topic')
    count = 0
    messages = []
    for message in consumer.iterqueue():
        messages.append(message)
        request = message.decode()
        request.path = convert_unicode_to_string(request.path[:255])
        request.data = convert_unicode_to_string(request.data[:255])
        request.referer = convert_unicode_to_string(request.referer[:255])
        request.user_agent =\
               convert_unicode_to_string(request.user_agent[:255])
        request.language = convert_unicode_to_string(request.language[:255])
        request.save()
        count += 1
    logger.info("Saved {0} requests".format(count))
    [m.ack() for m in messages]
    logger.debug("Acknowledged all messages")
    consumer.close()
    conn.close()
