import os

RABBIT_MQ_QUEUE = os.environ.get("RABBIT_MQ_QUEUE", "faststream-bridge")
RABBIT_MQ_URL = os.environ.get("RABBIT_MQ_URL", "amqp://guest:guest@localhost:5672/")