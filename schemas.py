from pydantic import BaseModel, Field
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, ForeignKey
from typing import List
from datetime import date


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    job: Mapped[str] = mapped_column(String)
    information_items: Mapped[List["InformationalModel"]] = relationship(back_populates="user")


class UserPostSchema(BaseModel):
    nickname: str = Field(..., title="Никнейм", description="Никнейм пользователя (максимум 20 символов)",
                            min_length=1, max_length=20, examples=["Nickname"])
    first_name: str = Field(..., title="Имя", description="Имя пользователя (максимум 20 символов)",
                            min_length=1, max_length=20, examples=["Name"])
    last_name: str = Field(..., title="Фамилия", description="Фамилия пользователя (максимум 20 символов)",
                           min_length=1, max_length=20, examples=["Surname"])
    age: int = Field(..., title="Возраст", description="Возраст пользователя (от 1 до 99 лет)", ge=1, le=99,
                     examples=["50"])
    job: str = Field(..., title="Работа", description="Работа пользователя (максимум 100 символов)", min_length=1,
                     max_length=100, examples=["Worker"])


class UserGetSchema(BaseModel):
    nickname: str
    first_name: str
    last_name: str
    age: int
    job: str


class UserPutSchema(BaseModel):
    age: int = Field(..., title="Возраст", description="Возраст пользователя (от 1 до 99 лет)", ge=1, le=99,
                     examples=["50"])
    job: str = Field(..., title="Работа", description="Работа пользователя (максимум 100 символов)", min_length=1,
                     max_length=100, examples=["Worker"])


class InformationalModel(Base):
    __tablename__ = "information"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    information: Mapped[str] = mapped_column(String)
    explanation: Mapped[str] = mapped_column(String)
    repeat_date_1: Mapped[date] = mapped_column(Date)
    repeat_date_2: Mapped[date] = mapped_column(Date)
    repeat_date_3: Mapped[date] = mapped_column(Date)
    repeat_date_4: Mapped[date] = mapped_column(Date)
    repeat_date_5: Mapped[date] = mapped_column(Date)
    user_nickname: Mapped[str] = mapped_column(ForeignKey("users.nickname", ondelete="CASCADE"))
    user: Mapped["UserModel"] = relationship(back_populates="information_items")


class InformationPostSchema(BaseModel):
    information: str = Field(..., title="Тезис", description="Имя пользователя (максимум 30 символов)",
                             min_length=1, max_length=30, examples=["What is QA"])
    explanation: str = Field(..., title="Объяснение", description="Имя пользователя (максимум 200 символов)",
                             min_length=1, max_length=200, examples=[
            "QA is Quality Assurance that means that we control the quality of product during all steps of developing"])


class InformationGetSchema(BaseModel):
    id: int
    information: str
    explanation: str
    repeat_date_1: date
    repeat_date_2: date
    repeat_date_3: date
    repeat_date_4: date
    repeat_date_5: date
    user_nickname: str


class Status(BaseModel):
    status: str = Field(..., examples=["success"], title="Status")
