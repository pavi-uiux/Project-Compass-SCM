from confluent_kafka import Consumer
from config import KAFKA_BOOTSTRAP, KAFKA_KEY, KAFKA_SECRET, KAFKA_TOPIC_IN_TRANSIT, KAFKA_TOPIC_ARRIVAL, KAFKA_TOPIC_CUSTOMS, KAFKA_TOPIC_DELIVERED
import json

conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': KAFKA_KEY,
    'sasl.password': KAFKA_SECRET,
    'group.id': 'project_compass_demo',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
topics = [KAFKA_TOPIC_IN_TRANSIT, KAFKA_TOPIC_ARRIVAL, KAFKA_TOPIC_CUSTOMS, KAFKA_TOPIC_DELIVERED]
consumer.subscribe(topics)

print("📡 Listening to Kafka topics for Project Compass demo...")

try:
    while True:
        msg = consumer.poll(1.0)  # 1 second timeout
        if msg is None:
            continue
        if msg.error():
            print(f"⚠️ Error: {msg.error()}")
            continue

        data = json.loads(msg.value().decode('utf-8'))
        print(f"✅ Topic: {msg.topic()} | Message: {json.dumps(data, indent=2)}")

except KeyboardInterrupt:
    print("🛑 Stopping Kafka consumer demo")
finally:
    consumer.close()
