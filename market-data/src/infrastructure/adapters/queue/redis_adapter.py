import logging
import json
import os

import redis
from dotenv import load_dotenv

load_dotenv()

ENV = os.environ.get("ENV", "DEV")


class RedisAdapter:
    def __init__(self, logger: logging.Logger) -> None:
        self.logger = logger
        self.host = os.environ.get(f"REDIS_HOST_{ENV}")
        self.port = os.environ.get(f"REDIS_PORT_{ENV}")
        self.redis_db = None
    
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
            self.logger.info(f"Connection with Redis was established, host: {self.host}:{self.port}")
            return self.redis_db
        except Exception as err:
            self.logger.error(f"Could not connect to Redis: {err}")

    
    def set_key(self, query, data):
        """
        Set key to Redis
        """
        if self.redis_db:
            try:
                self.redis_db.set(query, data)
                self.logger.debug(f"Key: {query}, Value: {data}")
            except Exception as err:
                self.logger.error(f"Could not add data to query: {err}")
    

    def append_to_set(self, query, data, send_time):
        if self.redis_db:
            key_type = self.redis_db.type(query).decode('utf-8')
            self.logger.debug(f"key_type: {key_type}")
            try:
                self.redis_db.zadd(query, {json.dumps(data): send_time})
                self.logger.info(f"Time to expire set: {self.redis_db.ttl(query)}")
                if self.redis_db.ttl(query) == -1:
                    self.redis_db.expire(query, int(60*60*24*2)) # expires in two days
                self.logger.info(f"Appended data to Redis set '{query}': {json.dumps(data)}, send_time: {send_time}")
            except Exception as err:
                self.logger.info(f"Could not append data to redis, reason: {err}")


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

    
    def get_queue(self, queue):
        message_data = self.redis_db.rpop(queue)
        self.logger.debug(f"Consumed data from queue: {queue}, data: {message_data}")
        if not message_data:
            self.logger.debug(f"Queue '{queue}' is empty or no messages fetched.")
            return {"status": False, "message": {}}
        
        message_json = json.loads(message_data)
        return {"status": True, "message": message_json}


    def get_batch_queue(self, queue, count=100):
        messages_data = self.redis_db.rpop(queue, count)  # Attempt to pop up to `count` messages

        self.logger.debug(f"Consumed {len(messages_data) if messages_data else 0} messages from queue: {queue}")

        if not messages_data:
            self.logger.debug(f"Queue '{queue}' is empty or no messages fetched.")
            return {"status": False, "messages": []}

        # Convert JSON strings to Python dictionaries
        messages_json = [json.loads(msg) for msg in messages_data]
        
        return {"status": True, "messages": messages_json}
    
    
    def insert_to_queue(self, message_data, queue):
        message_json = json.dumps(message_data, default=str)
        try:
            self.redis_db.lpush(queue, message_json)
            self.logger.debug(f"Inserted data into queue: {queue}, {message_json}")
        except Exception as err:
            self.logger.error(f"Could not insert data into Redis queue, reason: {err}")

    def publish_message(self, channel: str, message_data: dict) -> bool:
        message = json.dumps(message_data)
        self.redis_db.publish(channel, message)