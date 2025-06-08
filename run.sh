#!/bin/bash

# Start Kafka
docker-compose up -d

# Wait for Kafka
sleep 20

# Create topic
docker exec kafka kafka-topics --create \
  --topic cookies \
  --partitions 1 \
  --bootstrap-server localhost:9092

# Install dependencies
pip install -r producer/requirements.txt
pip install -r consumer/requirements.txt

# Run in parallel
(trap 'kill 0' SIGINT; \
 python producer/producer.py & \
 python consumer/consumer.py)
