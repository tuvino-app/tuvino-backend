import fastapi
import logging
import math
from fastapi import status, HTTPException, Path, Query
from src.models.schemas.wine import WineSchema, WineFilters, PaginatedWineResponse
from src.repository.wines_repository import WinesRepository

router = fastapi.APIRouter(prefix="/wines", tags=["wines"])
repo = WinesRepository()

@router.get(
    "/search",
    summary="Get wines by filters with pagination",
    response_model=PaginatedWineResponse,
    status_code=status.HTTP_200_OK,
)
async def get_wine_by_name(wine_name: str = Query(None, description="Wine name"),
                           wine_type: str = Query(None, description="Type of wine"),
                           winery: str = Query(None, description="Name of winery"),
                           country: str = Query(None, description="Region of origin"),
                           region: str = Query(None, description="Region of origin"),
                           min_abv: float = Query(None, description="Minimum ABV"),
                           max_abv: float = Query(None, description="Maximum ABV"),
                           page: int = Query(1, ge=1, description="Page number (starting from 1)"),
                           page_size: int = Query(20, ge=1, le=100, description="Number of items per page")):
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

        # Calculate offset from page number
        offset = (page - 1) * page_size

        # Get paginated wines and total count
        wines, total = repo.get_by_filters(filters, limit=page_size, offset=offset)

        # Calculate pagination metadata
        total_pages = math.ceil(total / page_size) if total > 0 else 0
        has_next = page < total_pages
        has_previous = page > 1

        return PaginatedWineResponse(
            items=wines,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous
        )

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