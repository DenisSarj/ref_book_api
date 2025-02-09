import re

from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates, mapped_column, Mapped, relationship

from src.app.repositories.db.models.base import Base
from src.app.repositories.db.models.mixins.int_id_pk import IntIdPkMixin


class PhoneNumber(IntIdPkMixin, Base):
    number: Mapped[str] = mapped_column(nullable=False, unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"), nullable=False)

    organization: Mapped["Organization"] = relationship(back_populates="phone_numbers")

    def __str__(self):
        return f"<PhoneNumber(number={self.number}, organization_id={self.organization_id})>"

    def __repr__(self):
        return self.__str__()

    @validates("number")
    def validate_phone_number(self, key, value):
        pattern = r"^\+(\d)-\((\d{3})\)-(\d{3})-(\d{2})-(\d{2})$"
        if not re.match(pattern, value):
            raise ValueError(f"[X] Неверный формат номера телефона: {value}")
        return value
