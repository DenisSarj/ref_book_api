import re

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr

from src.configs import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.database.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__camel_case_to_snake_case(cls.__name__)}"

    @classmethod
    def __camel_case_to_snake_case(cls, name: str) -> str:
        snake_name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return f"{snake_name}es" if snake_name.endswith("s") else f"{snake_name}s"
