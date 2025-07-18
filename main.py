from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from typing import Annotated, List
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Depends, HTTPException, Request
from schemas import Base, UserModel, UserGetSchema, UserPostSchema, UserPutSchema, InformationalModel, \
    InformationPostSchema, InformationGetSchema, Status
from datetime import date, timedelta
from fastapi.openapi.utils import get_openapi

app = FastAPI(title="Forgetting-Curve API",
              description="Available API methods for Forgetting-Curve",
              version="1.0.4",
              openapi_tags=[
                  {"name": "Users", "description": "Операции с пользователями"},
                  {"name": "Users information", "description": "Операции с информацией пользователей"},
              ])
engine = create_async_engine("sqlite+aiosqlite:///users.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Forgetting-Curve API",
        version="1.0.4",
        description="Available API methods for Forgetting-Curve",
        routes=app.routes,
    )
    # Remove 422 responses
    for path in openapi_schema["paths"].values():
        for method in path.values():
            if "422" in method["responses"]:
                del method["responses"]["422"]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = exc.errors()
    formatted_errors = [{"loc": error["loc"], "msg": error["msg"]} for error in details]

    raise HTTPException(status_code=400, detail=formatted_errors)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


@app.post("/setup_database", tags=["Options"], summary="Очистка и создание новой пустой базы данных")
async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    return {"status": "success"}


@app.post("/users", tags=["Users"], summary="Создание нового пользователя", response_model=None,
          description="Этот эндпоинт создает нового пользователя в базе данных",
          responses={
              200: {
                  "description": "Успешный ответ. Возвращает статус 'успех'",
                  "model": Status,
                  "content": {
                      "application/json": {
                          "example": {"status": "success"}
                      }
                  }
              },
              400: {
                  "description": "Ошибка валидации",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": [
                                  {
                                      "loc": [
                                          "body",
                                          "field"
                                      ],
                                      "msg": "string"
                                  }
                              ]
                          }
                      }
                  }
              }
          })
async def create_user(data: UserPostSchema, session: SessionDep):
    try:
        new_user = UserModel(
            nickname=data.nickname,
            first_name=data.first_name,
            last_name=data.last_name,
            age=data.age,
            job=data.job
        )
        session.add(new_user)
        await session.commit()
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users", response_model=List[UserGetSchema], tags=["Users"],
         summary="Получение списка всех пользователей",
         description="Этот эндпоинт возвращает список всех зарегистрированных пользователей",
         responses={
             200: {
                 "nickname": "string",
                 "first_name": "string",
                 "last_name": "string",
                 "age": 0,
                 "job": "string"

             }
         })
async def get_list_of_users(session: SessionDep):
    query = select(UserModel)
    result = await session.execute(query)
    return result.scalars().all()


@app.get("/users/{nickname}", response_model=UserGetSchema, tags=["Users"],
         summary="Получение конкретного пользователя",
         description="Этот эндпоинт возвращает данные о конкретном пользователе",
         response_description="Успешный ответ. Возвращает конкретного пользователя")
async def get_user(nickname: str, session: SessionDep):
    user = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@app.put("/users/{nickname}", tags=["Users"], summary="Обновление данных о пользователе",
         description="Этот эндпоинт обновляет возраст и работу конкретного пользователя",
         responses={
             200: {
                 "description": "Успешный ответ. Возвращает статус 'успех'",
                 "model": Status,
                 "content": {
                     "application/json": {
                         "example": {"status": "success"}
                     }
                 }
             },
             400: {
                 "description": "Ошибка валидации",
                 "content": {
                     "application/json": {
                         "example": {
                             "detail": [
                                 {
                                     "loc": [
                                         "body",
                                         "field"
                                     ],
                                     "msg": "string"
                                 }
                             ]
                         }
                     }
                 }
             },
             404: {
                 "detail": "User not found"
             }
         })
async def update_user(nickname: str, data: UserPutSchema, session: SessionDep):
    user = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        user.age = data.age
        user.job = data.job
        await session.commit()
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/users/{nickname}", tags=["Users"], summary="Удаление пользователя",
            description="Этот эндпоинт удаляет конкретного пользователя из базы данных",
            responses={
                200: {
                    "description": "Успешный ответ. Возвращает статус 'успех'",
                    "model": Status,
                    "content": {
                        "application/json": {
                            "example": {"status": "success"}
                        }
                    }
                },
                400: {
                    "description": "Ошибка валидации",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": [
                                    {
                                        "loc": [
                                            "body",
                                            "field"
                                        ],
                                        "msg": "string"
                                    }
                                ]
                            }
                        }
                    }
                },
                404: {
                    "detail": "User not found"
                }
            })
async def delete_user(nickname: str, session: SessionDep):
    user = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return {"status": "success"}


@app.post("/users/{nickname}/information", tags=["Users information"],
          summary="Создание информации для конкретного пользователя",
          description="Этот эндпоинт создает тезис и объяснение для конкретного пользователя",
          responses={
              200: {
                  "description": "Успешный ответ. Возвращает статус 'успех'",
                  "model": Status,
                  "content": {
                      "application/json": {
                          "example": {"status": "success"}
                      }
                  }
              },
              400: {
                  "description": "Ошибка валидации",
                  "content": {
                      "application/json": {
                          "example": {
                              "detail": [
                                  {
                                      "loc": [
                                          "body",
                                          "field"
                                      ],
                                      "msg": "string"
                                  }
                              ]
                          }
                      }
                  }
              },
              404: {
                  "detail": "User not found"
              }
          })
async def create_information(nickname: str, data: InformationPostSchema, session: SessionDep):
    user = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    today = date.today()
    new_information = InformationalModel(
        information=data.information,
        explanation=data.explanation,
        repeat_date_1=today + timedelta(hours=1),
        repeat_date_2=today + timedelta(days=1),
        repeat_date_3=today + timedelta(days=4),
        repeat_date_4=today + timedelta(days=15),
        repeat_date_5=today + timedelta(days=30),
        user_nickname=nickname
    )
    session.add(new_information)
    await session.commit()
    return {"status": "success"}


@app.get("/users/{nickname}/information", response_model=List[InformationGetSchema], tags=["Users information"],
         summary="Получение списка информации у пользователя",
         description="Этот эндпоинт возвращает список всей информации у конкретного пользователя",
         responses={
             200: {
                 "description": "Успешный ответ. Возвращает статус 'успех'",
                 "model": Status,
                 "content": {
                     "application/json": {
                         "example": {"status": "success"}
                     }
                 }
             },
             400: {
                 "description": "Ошибка валидации",
                 "content": {
                     "application/json": {
                         "example": {
                             "detail": [
                                 {
                                     "loc": [
                                         "body",
                                         "field"
                                     ],
                                     "msg": "string"
                                 }
                             ]
                         }
                     }
                 }
             },
             404: {
                 "detail": "User not found"
             }
         })
async def get_user_information(nickname: str, session: SessionDep):
    user = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = select(InformationalModel).where(InformationalModel.user_nickname == nickname)
    result = await session.execute(query)
    information_items = result.scalars().all()

    information_get_schemas = [
        InformationGetSchema(
            id=item.id,
            information=item.information,
            explanation=item.explanation,
            repeat_date_1=item.repeat_date_1,
            repeat_date_2=item.repeat_date_2,
            repeat_date_3=item.repeat_date_3,
            repeat_date_4=item.repeat_date_4,
            repeat_date_5=item.repeat_date_5,
            user_nickname=item.user_nickname
        )
        for item in information_items
    ]

    return information_get_schemas


@app.delete("/users/{nickname}/information/{information_id}", tags=["Users information"],
            summary="Удаление информации у пользователя",
            description="Этот эндпоинт удаляет конкретную информацию у конкретного пользователя",
            responses={
                200: {
                    "description": "Успешный ответ. Возвращает статус 'успех'",
                    "model": Status,
                    "content": {
                        "application/json": {
                            "example": {"status": "success"}
                        }
                    }
                },
                400: {
                    "description": "Ошибка валидации",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": [
                                    {
                                        "loc": [
                                            "body",
                                            "field"
                                        ],
                                        "msg": "string"
                                    }
                                ]
                            }
                        }
                    }
                },
                404: {
                    "detail": "User not found"
                }
            })
async def delete_information(nickname: str, information_id: int, session: SessionDep):
    user = await session.execute(select(UserModel).where(UserModel.nickname == nickname))
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    information = await session.execute(
        select(InformationalModel)
        .where(InformationalModel.user_nickname == nickname)
        .where(InformationalModel.id == information_id)
    )
    information = information.scalar_one_or_none()

    if not information:
        raise HTTPException(status_code=404, detail="Information not found")

    await session.delete(information)
    await session.commit()
    return {"status": "success"}
