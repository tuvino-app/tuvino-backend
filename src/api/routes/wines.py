import fastapi
import logging
from fastapi import status, HTTPException, Path, Query
from src.models.schemas.wine import WineSchema, WineFilters
from src.repository.wines_repository import WinesRepository

router = fastapi.APIRouter(prefix="/wines", tags=["wines"])
repo = WinesRepository()

@router.get(
    "/search",
    summary="Get wines by wine_name",
    response_model=list[WineSchema],
    status_code=status.HTTP_200_OK,
)
async def get_wine_by_name(wine_name: str = Query(None, description="Wine name"),
                           wine_type: str = Query(None, description="Type of wine"),
                           winery: str = Query(None, description="Name of winery"),
                           country: str = Query(None, description="Region of origin"),
                           region: str = Query(None, description="Region of origin"),
                           min_abv: float = Query(None, description="Minimum ABV"),
                           max_abv: float = Query(None, description="Maximum ABV")):
    try:
        filters = WineFilters(
            wine_name=wine_name,
            wine_type=wine_type,
            winery=winery,
            country=country,
            region=region,
            min_abv=min_abv,
            max_abv=max_abv
        )

        wines = repo.get_by_filters(filters)

        if not wines:
            raise HTTPException(
                status_code=404,
                detail="No wines found matching the criteria"
            )

        return wines

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Error retrieving wines: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving wines"
        )

@router.get(
    "/{wine_id}",
    summary="Get wine by wine_id",
    response_model=WineSchema,
    status_code=status.HTTP_200_OK,
)
async def get_wine_by_id(wine_id: int = Path(..., description="Wine ID")):
    wine = repo.get_by_id(wine_id)
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return wine

@router.post(
    "/",
    summary="Create a new wine",
    response_model=WineSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_wine(wine: WineSchema):
    new_wine = repo.create(wine)
    if not new_wine:
        raise HTTPException(status_code=400, detail="Wine not created")
    return new_wine

@router.put(
    "/{wine_id}",
    summary="Update wine by wine_id",
    response_model=WineSchema,
    status_code=status.HTTP_200_OK,
)
async def update_wine(wine_id: int, wine_data: dict):
    updated_wine = repo.update_by_id(wine_id, wine_data)
    if not updated_wine:
        raise HTTPException(status_code=404, detail="Wine not updated")
    return updated_wine

@router.delete(
    "/{wine_id}",
    summary="Delete wine by wine_id",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_wine(wine_id: int):
    success = repo.delete_by_id(wine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Wine not deleted")
    return None