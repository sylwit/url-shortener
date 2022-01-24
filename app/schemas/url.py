from pydantic import BaseModel
from pydantic import AnyHttpUrl


class Url(BaseModel):
    url: AnyHttpUrl
