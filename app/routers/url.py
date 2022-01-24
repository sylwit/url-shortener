import logging

from botocore.exceptions import ClientError
from pydantic import ListUniqueItemsError
from pynamodb.exceptions import PutError
from retry import retry

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse

from app.models.url import UrlTable
from app.schemas.url import Url

from app.settings import config

router = APIRouter()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


@router.get("/{hashid}", status_code=status.HTTP_307_TEMPORARY_REDIRECT)
async def get(hashid):
    item = list(UrlTable.hashid_index.query(hashid, limit=1))
    if not item:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    location = item[0].attribute_values.get("url")

    return RedirectResponse(location)


@router.post("/url", response_model=Url, status_code=status.HTTP_201_CREATED)
async def add(data: Url):
    url = UrlTable(url=data.url)
    url.generate_hashid()

    # Simulate a collision
    # url.hashid = "KwaMv8A2a7E"

    @retry(ListUniqueItemsError, tries=5)
    def prevalidate():
        logging.info(f"testing hashid {url.hashid}")
        hashid_exist = set(url.hashid_index.query(url.hashid, limit=1))
        if hashid_exist:
            logging.info(f"hashid_exist {url.hashid}: {hashid_exist}")
            url.generate_hashid()
            raise ListUniqueItemsError

    try:
        prevalidate()

        logging.info(f"before saving")
        url.save(UrlTable.url.does_not_exist())
    except ListUniqueItemsError as e:
        logging.error("We found 5 successive collisions !!!")
        return JSONResponse(content={"err": "We can't add this URL for now"}, status_code=status.HTTP_409_CONFLICT)
    except PutError as e:
        if isinstance(e.cause, ClientError):
            code = e.cause.response['Error'].get('Code')
            logging.info("url has been refreshed from db - signature already exists")
            if code == "ConditionalCheckFailedException":
                url.refresh()

    return Url(url=f"{config.DOMAIN}/{url.hashid}")
