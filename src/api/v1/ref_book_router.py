from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.app.common.services import RefBookSourceService
from src.app.repositories.db.models.db_helper import db_helper
from src.app.schemas.ref_book_schemas import OrganizationBase, OrganizationsResponse

router = APIRouter(prefix="/ref_book", tags=["ref_book"])


def get_ref_book_service() -> RefBookSourceService:
    return RefBookSourceService()


@router.get("/organizations/fetch/by_building_id/{building_id}", response_model=OrganizationsResponse)
async def get_organizations_by_building(
        building_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        ref_book_source_service: RefBookSourceService = Depends(get_ref_book_service)
):
    organizations = await ref_book_source_service.get_organizations_by_building(session, building_id)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return OrganizationsResponse(organizations=[OrganizationBase.model_validate(org) for org in organizations])


@router.get("/organizations/fetch/by_activity_id/{activity_id}", response_model=OrganizationsResponse)
async def get_organizations_by_activity(
        activity_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        ref_book_source_service: RefBookSourceService = Depends(get_ref_book_service)
):
    organizations = await ref_book_source_service.get_organizations_by_activity(session, activity_id)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return OrganizationsResponse(organizations=[OrganizationBase.model_validate(org) for org in organizations])


@router.get("/organizations/fetch/by_radius", response_model=OrganizationsResponse)
async def get_organizations_by_radius(
        lat: float,
        lon: float,
        radius: float,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        ref_book_source_service: RefBookSourceService = Depends(get_ref_book_service)
):
    organizations = await ref_book_source_service.get_organizations_by_radius(
        session=session,
        lat=lat,
        lon=lon,
        radius=radius
    )
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return OrganizationsResponse(organizations=[OrganizationBase.model_validate(org) for org in organizations])


@router.get("/organization/fetch/by_id/{organization_id}", response_model=OrganizationBase)
async def get_organization_by_id(
        organization_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        ref_book_source_service: RefBookSourceService = Depends(get_ref_book_service)
):
    organization = await ref_book_source_service.get_organization_by_id(session, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return OrganizationBase.model_validate(organization)


@router.get("/organizations/fetch/by_activity_tree/{activity_name}", response_model=OrganizationsResponse)
async def get_organizations_by_activity_tree(
        activity_name: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        ref_book_source_service: RefBookSourceService = Depends(get_ref_book_service)
):
    organizations = await ref_book_source_service.get_organizations_by_activity_tree(session, activity_name)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return OrganizationsResponse(organizations=[OrganizationBase.model_validate(org) for org in organizations])


@router.get("/organizations/fetch/by_name/{name}", response_model=OrganizationsResponse)
async def get_organizations_by_name(
        name: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
        ref_book_source_service: RefBookSourceService = Depends(get_ref_book_service)
):
    organizations = await ref_book_source_service.get_organizations_by_name(session, name)
    if not organizations:
        raise HTTPException(status_code=404, detail="Organizations not found")
    return OrganizationsResponse(organizations=[OrganizationBase.model_validate(org) for org in organizations])
