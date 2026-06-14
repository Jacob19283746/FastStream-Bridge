# FastStream Bridge

Сервис принимает **GET**-запросы с **любыми** query-параметрами, обрабатывает их и отправляет **JSON** в очередь RabbitMQ **`fastapi_bridge`**.

Имена полей не фиксированы — можно передать что угодно, например:

```http
GET http://localhost:8000/?phone_number=79000000000&message_text=Hello+World!
GET http://localhost:8000/?order_id=42&status=new&comment=срочно
```

В Swagger ([/docs](http://localhost:8000/docs)) показаны примеры полей (`phone_number`, `name`, `message_text`). Это не полный список — остальные ключи можно передавать в URL.

## Обработка данных

Перед отправкой в RabbitMQ сервис приводит query-параметры к единому виду:

1. **Сбор** — все пары ключ/значение из URL (в том числе повторяющиеся ключи).
2. **Нормализация:**
   - у каждого **ключа** и **значения** обрезаются пробелы по краям;
   - параметры с **пустым именем** (только пробелы) отбрасываются;
   - один ключ в URL → строка в JSON, тот же ключ повторно → массив строк (например `?tag=a&tag=b` → `"tag": ["a", "b"]`).
3. **Публикация** — итоговый словарь сериализуется в JSON и кладётся в `fastapi_bridge`.


## Зависимости

- Python 3.13+
- FastAPI, Pydantic
- Faststream
- uvicorn
- RabbitMQ (в Docker поднимается автоматически)

## Запуск

```bash
docker compose up --build
```

| Сервис   | Адрес                    |
|----------|--------------------------|
| API      | http://localhost:8000    |
| RabbitMQ | http://localhost:15672   |

Остановка: `docker compose down`

## Проверка в веб-интерфейсе RabbitMQ

1. Откройте [http://localhost:15672](http://localhost:15672)
2. Войдите: `guest` / `guest`
3. Отправьте запрос:

```bash
curl "http://localhost:8000/?phone_number=79000000000&message_text=Hello+World!"
```

4. В RabbitMQ: **Queues** → **handler-queue** → **Get messages**

В очереди должно появиться:

```json
{"phone_number": "79000000000", "message_text": "Hello World!"}
```

Ответ API дублирует то, что ушло в очередь:

```json
{
  "status_code": 200,
  "message": "Successfully submitted parameters to the queue",
  "detail": { "phone_number": "79000000000", "message_text": "Hello" }
}
```
