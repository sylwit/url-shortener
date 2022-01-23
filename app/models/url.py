from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model

from app.settings import config


class BaseTable(Model):
    class Meta:
        host = config.DB_HOST
        region = config.AWS_REGION


class UrlTable(BaseTable):
    """
    Represents a DynamoDB table for an URL
    """

    class Meta(BaseTable.Meta):
        table_name = "url"

    signature = UnicodeAttribute(hash_key=True)
