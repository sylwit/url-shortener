import time
import hashlib
from hashids import Hashids

from pynamodb.attributes import UnicodeAttribute
from pynamodb.indexes import AllProjection
from pynamodb.indexes import GlobalSecondaryIndex
from pynamodb.models import Model

from app.settings import config

hashids = Hashids(salt=config.HASH_SALT)


class BaseTable(Model):
    class Meta:
        host = config.DB_HOST
        region = config.AWS_REGION


class HashidIndex(GlobalSecondaryIndex["UrlTable"]):
    """
    Represents a global secondary index for UrlTable
    """

    class Meta:
        read_capacity_units = 1
        write_capacity_units = 1
        projection = AllProjection()

    hashid = UnicodeAttribute(hash_key=True)


class UrlTable(BaseTable):
    """
    Represents a DynamoDB table for an URL
    """

    class Meta(BaseTable.Meta):
        table_name = "url"
        read_capacity_units = 1
        write_capacity_units = 1

    url = UnicodeAttribute(hash_key=True)
    hashid = UnicodeAttribute(null=False)
    hashid_index = HashidIndex()

    def generate_hashid(self):
        now = int(time.time() * 1000)
        epoch = 1641042000000  # Saturday, January 1, 2022 1:00:00 PM
        signature = hashlib.sha256(self.url.encode('utf-8')).hexdigest()
        shard = int(signature[:5], 16)  # max 20 bits

        tmp_id = (now - epoch) << (64 - 44)
        tmp_id |= shard

        self.hashid = hashids.encode(tmp_id)
