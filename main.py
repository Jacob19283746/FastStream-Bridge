from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.rabbit import RabbitQueue

from app.routers import router
from app.settings import RABBIT_MQ_QUEUE


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await router.broker.start()

    queue = RabbitQueue(name=RABBIT_MQ_QUEUE, durable=True)
    await router.broker.declare_queue(queue)

    yield
    await router.broker.close()


app = FastAPI(
    lifespan=lifespan,
    title="FastStream-RabbitMQ",
    description="RabbitMQ integration for [fast-stream](https://github.com/faststreamapi)"
)

app.include_router(router)
