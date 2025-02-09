from geoalchemy2 import WKTElement
from geoalchemy2.functions import ST_DWithin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import Optional, Sequence

from src.app.common.loggers import setup_file_logger
from src.app.repositories.db.models import Building
from src.app.repositories.db.models.organization import Organization
from src.app.repositories.db.models.activity import Activity


class RefBookSourceService:
    def __init__(self):
        self.__logger = setup_file_logger("RefBookSourceService", "ref_book_source_service.log")

    async def get_organizations_by_building(
            self,
            session: AsyncSession,
            building_id: int
    ) -> Sequence[Organization]:
        try:
            stmt = (
                select(Organization)
                .filter(Organization.building_id == building_id)
                .options(selectinload(Organization.phone_numbers))
            )
            result = await session.scalars(stmt)
            return result.all()
        except Exception as e:
            self.__logger.error(f"[X] Ошибка при получении организаций по зданию {building_id}: {e}")
            raise

    async def get_organizations_by_activity(
            self,
            session: AsyncSession,
            activity_id: int
    ) -> Sequence[Organization]:
        try:
            stmt = (
                select(Organization)
                .filter(Organization.activity_id == activity_id)
                .options(selectinload(Organization.phone_numbers))
            )
            result = await session.scalars(stmt)
            return result.all()
        except Exception as e:
            self.__logger.error(f"[X] Ошибка при получении организаций по виду деятельности {activity_id}: {e}")
            raise

    async def get_organizations_by_radius(
            self,
            session: AsyncSession,
            lat: float,
            lon: float,
            radius: float
    ) -> Sequence[Organization]:
        try:
            point = WKTElement(f"POINT({lon} {lat})")
            stmt = (
                select(Organization)
                .join(Building)
                .filter(ST_DWithin(Building.location, point, radius))
                .options(selectinload(Organization.phone_numbers))
            )
            result = await session.scalars(stmt)
            return result.all()
        except Exception as e:
            self.__logger.error(
                f"[X] Ошибка при получении организаций по радиусу {radius} от точки ({lat}, {lon}): {e}"
            )
            raise

    async def get_organizations_by_name(
            self,
            session: AsyncSession,
            name: str
    ) -> Sequence[Organization]:
        try:
            stmt = (
                select(Organization)
                .filter(Organization.name.ilike(f"%{name}%"))
                .options(selectinload(Organization.phone_numbers))
            )
            result = await session.scalars(stmt)
            return result.all()
        except Exception as e:
            self.__logger.error(f"[X] Ошибка при получении организаций по названию {name}: {e}")
            raise

    async def get_organization_by_id(
            self,
            session: AsyncSession,
            organization_id: int
    ) -> Optional[Organization]:
        try:
            stmt = (
                select(Organization)
                .filter(Organization.id == organization_id)
                .options(selectinload(Organization.phone_numbers))
            )
            result = await session.scalars(stmt)
            organization = result.first()
            if not organization:
                self.__logger.warning(f"Организация с id {organization_id} не найдена.")
            return organization
        except Exception as e:
            self.__logger.error(f"[X] Ошибка при получении организации по id {organization_id}: {e}")
            raise

    async def get_organizations_by_activity_tree(
            self,
            session: AsyncSession,
            activity_name: str
    ) -> Sequence[Organization]:
        try:
            stmt = select(Activity).filter(Activity.name == activity_name)
            result = await session.scalars(stmt)
            activity = result.first()
            if activity:
                activity_ids = [activity.id]
                stmt = select(Activity).filter(Activity.parent_id.in_(activity_ids))
                result = await session.scalars(stmt)
                child_activities = result.all()
                child_activity_ids = [act.id for act in child_activities]
                activity_ids.extend(child_activity_ids)

                stmt = (
                    select(Organization)
                    .filter(Organization.activity_id.in_(activity_ids))
                    .options(selectinload(Organization.phone_numbers))
                )
                result = await session.scalars(stmt)
                return result.all()
            else:
                self.__logger.warning(f"Вид деятельности с названием {activity_name} не найден.")
                return []
        except Exception as e:
            self.__logger.error(f"[X] Ошибка при получении организаций по виду деятельности {activity_name}: {e}")
            raise
