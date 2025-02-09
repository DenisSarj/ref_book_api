from typing import TYPE_CHECKING
from geoalchemy2 import Geometry
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.repositories.db.models.base import Base
from src.app.repositories.db.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from src.app.repositories.db.models.organization import Organization


class Building(IntIdPkMixin, Base):
    address: Mapped[str] = mapped_column(nullable=False, unique=True)
    location: Mapped[Geometry] = mapped_column(Geometry("POINT"), nullable=False, unique=False)

    organizations: Mapped[list["Organization"]] = relationship(back_populates="building", cascade="all, delete-orphan")

    def __str__(self):
        return self.address

    def __repr__(self):
        return self.__str__()
