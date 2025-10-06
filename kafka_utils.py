from confluent_kafka import Producer
import json
from datetime import datetime
from config import KAFKA_BOOTSTRAP, KAFKA_KEY, KAFKA_SECRET

# Kafka configuration with longer timeouts
conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': KAFKA_KEY,
    'sasl.password': KAFKA_SECRET,
    'socket.timeout.ms': 10000,      # 10 seconds socket timeout
    'message.timeout.ms': 30000      # 30 seconds message timeout
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"⚠️ Kafka delivery failed: {err}")
    else:
        print(f"✅ Message delivered to {msg.topic()} [{msg.partition()}]")

def serialize_for_kafka(data):
    """Convert datetime and non-serializable types"""
    def convert(o):
        if isinstance(o, datetime):
            return o.isoformat()
        return str(o)
    return json.loads(json.dumps(data, default=convert))

def send_to_kafka(topic, message):
    try:
        safe_message = serialize_for_kafka(message)
        producer.produce(
            topic,
            json.dumps(safe_message).encode('utf-8'),
            callback=delivery_report
        )
        producer.flush()
        print(f"📤 Sent to Kafka topic: {topic}")
    except Exception as e:
        # Instead of crashing, just log the error
        print(f"⚠️ Error sending to Kafka, message saved in DB anyway: {e}")
