from diagrams import Diagram, Cluster
from diagrams.kafka import Kafka
from diagrams.programming.language import Python
from diagrams.database import Redis

with Diagram("Cookie Monitor Architecture", show=False):
    with Cluster("Data Pipeline"):
        producer = Python("Producer")
        kafka = Kafka("Kafka")
        consumer = Python("Consumer")
        redis = Redis("Redis")

    dashboard = Python("Dashboard")
    
    producer >> kafka >> consumer >> redis
    redis >> dashboard
