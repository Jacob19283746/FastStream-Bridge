from fastapi import Request, HTTPException
from faststream.rabbit import RabbitQueue
from faststream.rabbit.fastapi import RabbitRouter

from app.normalise_params import normalize_query_params
from app.settings import RABBIT_MQ_QUEUE, RABBIT_MQ_URL

router = RabbitRouter(url=RABBIT_MQ_URL)

EXAMPLE_QUERY_PARAMS = [
    {
        "name": "Имя",
        "in": "query",
        "required": False,
        "schema": {
            "type": "string"
        },
        "description": "Имя пользователя"
        },
    {
        "name": "Возраст",
        "in": "query",
        "required": False,
        "schema": {
            "type": "integer",
            "minimum": 0,
            "maximum": 150
        },
        "description": "Возраст пользователя"
    }
]


@router.get(
    path="/",
    openapi_extra={"parameters": EXAMPLE_QUERY_PARAMS},
    description=f"Принимает **любые** query-параметры, нормализует и публикует в очередь RabbitMQ."
)
async def push_params_queue(request: Request):
    normalise_params: dict = await normalize_query_params(items=request.query_params.multi_items())
    if not normalise_params:
        raise HTTPException(
            status_code=400,
            detail="Необходимо передать хотя бы один параметр с непустым значением."
        )

    await router.broker.publish(
        message=normalise_params,
        queue=RabbitQueue(name=RABBIT_MQ_QUEUE, durable=True)
    )
    return {
        "status_code": 200,
        "message": "Параметр(ы) успешно добавлены в очередь RabbitMQ.",
        "detail": normalise_params
    }


@router.get(
    path="/health",
    description="Возвращает статус подключения к очереди RabbitMQ"
)
async def health_check():
    try:
        if router.broker._connection and not router.broker._connection.is_closed:
            return {
                "status_code": 200,
                "detail": "Успешное подключение к RabbitMQ."
            }
        else:
            raise HTTPException(
                status_code=503,
                detail="RabbitMQ не доступен, проверьте настройки."
            )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Необработанное исключение: {error}"
        )