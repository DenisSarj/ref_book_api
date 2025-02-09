import enum

from sqlalchemy import ForeignKey, event, select, exists, Enum
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.app.repositories.db.models.base import Base
from src.app.repositories.db.models.organization import Organization


class ActivityLevel(enum.Enum):
    LEVEL_1 = "Level 1"
    LEVEL_2 = "Level 2"
    LEVEL_3 = "Level 3"


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    parent_id = mapped_column(ForeignKey("activities.id"), nullable=True)
    level = mapped_column(Enum(ActivityLevel), nullable=False)

    parent = relationship("Activity", remote_side=[id], backref="sub_activities")

    organizations: Mapped[list[Organization]] = relationship(back_populates="activity")

    def __str__(self):
        return f"<Activity {self.name}>"

    def __repr__(self):
        return self.__str__()

    async def can_delete(self, session: AsyncSession) -> bool:
        stmt = select(exists().where(Organization.activity_id == self.id))

        result = await session.execute(stmt)
        return not result.scalar()


@event.listens_for(Activity, "before_delete")
def prevent_activity_delete_if_related(session: AsyncSession, target: Activity):
    if not target.can_delete(session):
        raise Exception(f"[X] Невозможно удалить деятельность {target.name}, пока к ней привязаны организации")
