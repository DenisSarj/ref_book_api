from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.repositories.db.models.base import Base
from src.app.repositories.db.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from src.app.repositories.db.models.building import Building
    from src.app.repositories.db.models.activity import Activity
    from src.app.repositories.db.models.phone_number import PhoneNumber


class Organization(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(512), nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))
    activity_id: Mapped[int] = mapped_column(ForeignKey("activities.id"))

    building: Mapped["Building"] = relationship(back_populates="organizations")
    activity: Mapped["Activity"] = relationship(back_populates="organizations")

    phone_numbers: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"<Organization(name={self.name}, building={self.building}, activity={self.activity})>"

    def __repr__(self):
        return self.__str__()
