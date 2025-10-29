from fastapi import FastAPI

from presentation.api import main_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="DDD Notification Service Python",
        description="Тестовое задание на сервис уведомлений",
        docs_url="/api/docs",
        debug=True,
    )

    app.include_router(main_router)

    return app
