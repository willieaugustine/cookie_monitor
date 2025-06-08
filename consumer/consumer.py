import json
import redis
from kafka import KafkaConsumer
from monitor import analyze_cookies  # Your existing analysis function

# Configure Redis connection
redis_client = redis.Redis(
    host='redis',  # Matches the docker-compose service name
    port=6379,
    db=0,
    decode_responses=True  # Automatically decode responses to strings
)

# Kafka consumer configuration
KAFKA_TOPIC = 'cookie_scans'
KAFKA_BOOTSTRAP_SERVERS = ['kafka:9092']  # Matches docker-compose service name

def create_consumer():
    """Create and return a Kafka consumer instance"""
    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        group_id='cookie-monitor-group'
    )

def store_results(scan_data):
    """Store scan results in Redis with proper data structure"""
    try:
        # Store latest scan
        redis_client.set('latest_scan', json.dumps(scan_data))
        
        # Add to scan history (list)
        redis_client.lpush('scan_history', json.dumps(scan_data))
        
        # Trim history to keep last 20 scans
        redis_client.ltrim('scan_history', 0, 19)
        
        # Store individual cookies in a hash for detailed access
        for cookie in scan_data.get('cookies', []):
            redis_client.hset(
                f"cookie:{cookie['name']}:{cookie['domain']}",
                mapping=cookie
            )
            
        print("Successfully stored results in Redis")
    except Exception as e:
        print(f"Error storing results in Redis: {str(e)}")

def process_message(message):
    """Process incoming Kafka message"""
    try:
        print(f"Received message at offset {message.offset}")
        scan_results = analyze_cookies(message.value)
        store_results(scan_results)
    except Exception as e:
        print(f"Error processing message: {str(e)}")

def start_consumer():
    """Main consumer loop"""
    consumer = create_consumer()
    print("Consumer started. Waiting for messages...")
    
    try:
        for message in consumer:
            process_message(message)
    except KeyboardInterrupt:
        print("Shutting down consumer...")
    finally:
        consumer.close()

if __name__ == '__main__':
    start_consumer()
