from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from domain.base.exceptions import ApplicationException
from logic.commands.user import CreateUserCommand
from logic.init import init_container
from logic.mediator import Mediator
from presentation.api.schemas import ErrorResponseSchema
from presentation.api.v1.user.schemas import (
    CreateUserRequestSchema,
    CreateUserResponseSchema,
)


router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт создаёт нового пользователя, если успешно, то пытается послать уведомления на все доступные контакты, если пользователь с таким username существует, то возвращается 400 ошибка",
    responses={
        status.HTTP_201_CREATED: {"model": CreateUserResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponseSchema},
    },
)
async def create_user_handler(
    schema: CreateUserRequestSchema,
    container=Depends(init_container),
):
    """Создать нового пользователя."""
    mediator: Mediator = container.resolve(Mediator)

    try:
        user, *_ = await mediator.handle_command(
            CreateUserCommand(
                username=schema.username,
                email=schema.email,
                telegram=schema.telegram,
                phone=schema.phone,
            ),
        )
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": exception.message},
        )

    return CreateUserResponseSchema.from_entity(user)
