import os
from typing import List
from . import properties_router

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from project.database import get_db_session
from project.properties.schemas import Property
from project.properties.crud import get_properties, get_property_by_user_id
from project.properties import crud, schemas, models
from project.users import crud
from project.users.schemas import UserBase, UserProperty
from project.utils.utilities import call_api
from project.security import get_current_user, RoleChecker
from project.config import settings


@properties_router.get('/properties-internal',
                       response_model=List[Property],
                       dependencies=[Depends(RoleChecker(["ADMIN"]))]
                       )
def read_properties_internal(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    """
    Retrieve all properties.

    NOTE: Admin-level only
    """
    properties = get_properties(db, skip=skip, limit=limit)
    return properties


@properties_router.get('/user-property-internal',
                       response_model=UserProperty,
                       )
def read_user_property_internal(
        current_user: UserBase = Depends(get_current_user),
        db: Session = Depends(get_db_session)
):
    """
    Retrieve currently authenticated user's property.

    NOTE: Must be authenticated.
    """
    db_user = crud.get_user(db, user_id=current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user


@properties_router.get(
    '/property-details-external',
    dependencies=[Depends(RoleChecker(["ADMIN"]))]
)
async def read_any_property_details_from_external_api(
        external_source: schemas.ExternalSource,
        verbosity: schemas.PropertyDetailLeval,
        property_selection: schemas.PropertySelection,
):
    """
    Retrieve any property from external API.

    NOTE: Admin-level only
    """
    try:
        print(property_selection.value)
        if property_selection.value == 'All':
            result = await call_api(f'{settings.THIRD_PARTY_API}')
            if verbosity.value == 'Sewer System':
                return [{"property_address": obj["property_address"], "sewer_system": obj["property"]["sewer"]} for obj in result]
            return result

        else:
            result = await call_api(f'{settings.THIRD_PARTY_API}/{property_selection.value}')

            if verbosity.value == 'Sewer System':
                return {
                    "property_address": property_selection.value,
                    "sewer_system": result[0]["property"]["sewer"]
                }

            return result
    except:
        raise HTTPException(status_code=404, detail=f"The address {property_selection.value} was not found.")


@properties_router.get('/user-property-details-external')
async def read_user_property_details_from_external_api(
        external_source: schemas.ExternalSource,
        verbosity: schemas.PropertyDetailLeval,
        current_user: UserBase = Depends(get_current_user),
        db: Session = Depends(get_db_session)
):
    """
    Retrieve currently authenticated user's property details from external API.

    NOTE: Must be authenticated.
    """
    user_property = get_property_by_user_id(db, user_id=current_user.id)
    if not user_property:
        raise HTTPException(status_code=404, detail=f"The user {current_user.username} has no properties.")

    property_address = user_property.__dict__['property_address']

    result = await call_api(f'{settings.THIRD_PARTY_API}/{property_address}')

    if verbosity.value == 'Sewer System':
        return {
            "property_address": property_address,
            "sewer_system": result[0]["property"]["sewer"]
        }

    return result



