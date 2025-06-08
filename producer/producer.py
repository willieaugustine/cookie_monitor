from confluent_kafka import Producer
import time
import json
import random
import signal

# Configuration
conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)
shutdown_flag = False

# Cookie types for realistic data
cookie_types = ["chocolate_chip", "oatmeal", "sugar", "peanut_butter"]

# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    global shutdown_flag
    print("\nShutting down producer...")
    shutdown_flag = True

signal.signal(signal.SIGINT, signal_handler)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [Partition {msg.partition()}]")

# Optional: Set max messages (0 for unlimited)
MAX_MESSAGES = 20  
message_count = 0

print("Producer started (Press Ctrl+C to stop)")
while not shutdown_flag:
    if MAX_MESSAGES > 0 and message_count >= MAX_MESSAGES:
        print(f"Reached {MAX_MESSAGES} messages. Stopping...")
        break
        
    # Generate cookie event
    event = {
        "type": random.choice(cookie_types),
        "batch_id": random.randint(1000, 9999),
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "status": "fresh"
    }
    
    producer.produce(
        topic='cookies',
        value=json.dumps(event),
        callback=delivery_report
    )
    message_count += 1
    time.sleep(1)  # Throttle message rate

# Cleanup
producer.flush()
print(f"Producer stopped. Sent {message_count} messages.")
