
from kafka import KafkaConsumer

def consume_messages(topic):
    consumer = KafkaConsumer(topic)
    for message in consumer:
        print(message.value)
