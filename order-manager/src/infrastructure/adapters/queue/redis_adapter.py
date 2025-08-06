import logging
import json
import os

import redis
from dotenv import load_dotenv
import redis.client

load_dotenv()

ENV = os.environ.get("ENV", "DEV")


class RedisAdapter:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.host = os.environ.get(f"REDIS_HOST_{ENV}")
        self.port = os.environ.get(f"REDIS_PORT_{ENV}")

        self.redis_db = None
        self.pubsub = None
        self.subscriptions = {}
    
        self._create_connection()

    def _create_connection(self):
        """
        Create a connection with database.
        """
        self.logger.debug("Trying to connect with Redis")
        try:
            # Connect to Redis
            self.redis_db = redis.Redis(
                    host=self.host,
                    port=self.port,
                    ssl=False)
            
            # Check connection
            self.redis_db.ping()
            self.pubsub = self.redis_db.pubsub()
            self.logger.info(f"Connection with Redis was established, host: {self.host}:{self.port}")
            return self.redis_db
        except Exception as err:
            self.logger.error(f"Could not connect to Redis: {err}")

    def get_pubsub(self) -> redis.client.PubSub:
        return self.redis_db.pubsub()
    
    def set_key(self, query, data):
        """
        Set key to Redis
        """
        if self.redis_db:
            try:
                self.redis_db.set(query, data)
                self.logger.info(f"Key: {query}, Value: {data}")
            except Exception as err:
                self.logger.error(f"Could not add data to query: {err}")

    def get_key(self, key):
        """
        Get a key from Redis.
        """
        try:
            # Execute the Redis command to get the time series value
            search = self.redis_db.get(f"{key}")
            self.logger.debug(f"Found search: {search}")
            
            if search is None:
                self.logger.info(f"No data found for key: {key}")
                return None
            
            return json.loads(search)
        except Exception as err:
            self.logger.error(f"Error getting key from Redis: {err}")
            return None
    
    def insert_to_queue(self, message_data, queue):
        message_json = json.dumps(message_data, default=str)
        try:
            self.redis_db.lpush(queue, message_json)
            self.logger.debug(f"Inserted data into queue: {queue}, {message_json}")
        except Exception as err:
            self.logger.error(f"Could not insert data into Redis queue, reason: {err}")

    def publish_message(self, channel: str, message_data: dict = None) -> bool:
        message = json.dumps(message_data)
        self.redis_db.publish(channel, message)
    
    def subscribe(self, channel: str, callback: callable):
        self.pubsub.subscribe(channel)
        self.subscriptions[channel] = callback
    
    def unsubscribe(self, channel: str):
        self.pubsub.unsubscribe(channel)
    
    def start_listening(self):
        self.logger.info(f"[RedisAdapter] Listening to channels: {list(self.subscriptions)}")
        try:
            for message in self.pubsub.listen():
                if message["type"] == "message":
                    channel = message["channel"].decode()
                    data = json.loads(message["data"])
                    callback = self.subscriptions.get(channel)
                    if callback:
                        callback(data)
        except KeyboardInterrupt:
            self.logger.info("Stopped listening.")