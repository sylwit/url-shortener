from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.models.url import UrlTable

router = APIRouter()


@router.get("/{short_id}")
async def get(short_id):
    try:
        item = UrlTable.get(short_id)
    except UrlTable.DoesNotExist as e:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    # TODO :  make 302
    return item.attribute_values
