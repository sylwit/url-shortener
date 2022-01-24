# URL shortner with DynamoDB

## Build the docker image

> docker-compose build api

## Run

> docker-compose up api dbadmin

## Create database

> http://localhost:5000/db/init


## Test from swagger UI

> http://127.0.0.1:8000/docs

## Check dynamoDB with dbadmin

> http://127.0.0.1:8001

## Concepts

This API contains 2 endpoints
1 - POST /url for shortning an URL. This is done with a POST like bit.ly but using a GET with a query param could be easier to use
2 - GET /{hashid}, this route fetch in the dynamo GSI the URL corresponding to the hashid and sends an HTTP 307 temporary redirection

hashid are based on a 64bits integer generated randomly which will avoid any collision. This id is based on the timestamp in millisecond
and a "shard id". The shard id is the 5 first chars of the sha256 signature. This combination provides a pretty good entropy to avoid collisions
In case of a hypothetical collision, we successively retry with 5 others hashid.

## Infra

This POC relies on DynamoDB as primary Database to scale almost infinitely. The partition kay is based on the URL so provider the highest cardinality
as possible. Thanks to the global table, the database isn't restricted to a single region.
The application is totally stateless and dockerized, which means we can deploy as many containers, in any regions to make our application scales.

We will use a standard ALB -> Ec2 or any container engine (fargate, EKS)

Without data on the usage of our app it's hard to design the perfect architecture. With some data like:
- what are the most used hashid
- how often are they used
- what is the average lifetime of a hashid (mostly use for hours when it's created and shared, mostly months on high traffic websites, ...)
we could improve the cache mechanism by using DAX for example. 