import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.app.repositories.db.models.organization import Organization
from src.app.repositories.db.models.phone_number import PhoneNumber
from src.app.repositories.db.models.building import Building
from src.app.repositories.db.models.db_helper import db_helper
from src.app.repositories.db.models.activity import Activity, ActivityLevel
from src.app.common.loggers import debug_logger


async def create_test_data():
    async with db_helper.session_factory() as session:
        async with session.begin():
            activity1 = Activity(name="Строительство", level=ActivityLevel.LEVEL_1)
            activity2 = Activity(name="Информационные технологии", level=ActivityLevel.LEVEL_1)
            activity3 = Activity(name="Медицина", level=ActivityLevel.LEVEL_1)
            activity4 = Activity(name="Автомобили", level=ActivityLevel.LEVEL_1)
            activity5 = Activity(name="Еда", level=ActivityLevel.LEVEL_1)
            session.add_all([activity1, activity2, activity3, activity4, activity5])

            await session.commit()

    async with db_helper.session_factory() as session:
        async with session.begin():
            activity1_1 = Activity(name="Жилое строительство", level=ActivityLevel.LEVEL_2, parent_id=activity1.id)
            activity1_2 = Activity(name="Коммерческое строительство", level=ActivityLevel.LEVEL_2,
                                   parent_id=activity1.id)
            activity2_1 = Activity(name="Разработка ПО", level=ActivityLevel.LEVEL_2, parent_id=activity2.id)
            activity2_2 = Activity(name="Сетевые технологии", level=ActivityLevel.LEVEL_2, parent_id=activity2.id)
            activity3_1 = Activity(name="Больницы", level=ActivityLevel.LEVEL_2, parent_id=activity3.id)
            activity3_2 = Activity(name="Клиники", level=ActivityLevel.LEVEL_2, parent_id=activity3.id)
            activity4_1 = Activity(name="Грузовые автомобили", level=ActivityLevel.LEVEL_2, parent_id=activity4.id)
            activity4_2 = Activity(name="Легковые автомобили", level=ActivityLevel.LEVEL_2, parent_id=activity4.id)
            activity5_1 = Activity(name="Мясная продукция", level=ActivityLevel.LEVEL_2, parent_id=activity5.id)
            activity5_2 = Activity(name="Молочная продукция", level=ActivityLevel.LEVEL_2, parent_id=activity5.id)
            session.add_all(
                [activity1_1, activity1_2, activity2_1, activity2_2, activity3_1, activity3_2, activity4_1, activity4_2,
                 activity5_1, activity5_2])

            await session.commit()

    async with db_helper.session_factory() as session:
        async with session.begin():
            activity2_1_1 = Activity(name="Разработка мобильных приложений", level=ActivityLevel.LEVEL_3,
                                     parent_id=activity2_1.id)
            activity3_1_1 = Activity(name="Общественные больницы", level=ActivityLevel.LEVEL_3,
                                     parent_id=activity3_1.id)
            activity5_1_1 = Activity(name="Говядина", level=ActivityLevel.LEVEL_3, parent_id=activity5_1.id)
            session.add_all([activity2_1_1, activity3_1_1, activity5_1_1])

            await session.commit()

    async with db_helper.session_factory() as session:
        async with session.begin():
            building1 = Building(address="ул. Ленина, 10", location="POINT(37.6173 55.7558)")
            building2 = Building(address="ул. Пушкина, 5", location="POINT(37.6178 55.7559)")
            session.add_all([building1, building2])

            org1 = Organization(name="ООО 'Строитель'", building=building1, activity=activity1)
            org2 = Organization(name="ООО 'ТехноГрупп'", building=building2, activity=activity2_1)
            org3 = Organization(name="ООО 'Медицинские технологии'", building=building1, activity=activity3_1_1)
            org4 = Organization(name="ООО 'АвтоГруз'", building=building2, activity=activity4_2)
            org5 = Organization(name="ООО 'Молочная продукция'", building=building1, activity=activity2_1_1)
            session.add_all([org1, org2, org3, org4, org5])

            await session.commit()

    async with db_helper.session_factory() as session:
        async with session.begin():
            phone1 = PhoneNumber(number="+7-(999)-123-45-67", organization=org1)
            phone2 = PhoneNumber(number="+7-(999)-234-56-78", organization=org2)
            phone3 = PhoneNumber(number="+7-(999)-345-67-89", organization=org3)
            phone4 = PhoneNumber(number="+7-(999)-456-78-90", organization=org4)
            phone5 = PhoneNumber(number="+7-(999)-567-89-01", organization=org5)
            session.add_all([phone1, phone2, phone3, phone4, phone5])

            await session.commit()

        debug_logger.info("[#] Тестовые данные успешно добавлены!")


if __name__ == "__main__":
    asyncio.run(create_test_data())
