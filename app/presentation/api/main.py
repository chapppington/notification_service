from fastapi import FastAPI

from presentation.api.v1 import v1_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD Notification Service Python",
        description="Тестовое задание на сервис уведомлений",
        docs_url="/api/docs",
        debug=True,
    )

    app.include_router(v1_router)

    return app
