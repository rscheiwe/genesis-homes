# Genesis Homes - Feature Detection API

This API works in conjunction with the HomeBird API. 

Please review scope [here](https://github.com/rscheiwe/api-development/blob/main/README.md)


### Run locally without Celery:

```angular2html
$ uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8002
```

### Run via Docker to enable Celery:

```angular2html
$ docker-compose up -d --build
```


### For DB Migrations and data seeding:

Alembic is used for DB migrations, and seeding is done via `project/utils/seed.py`.

To start from scratch: 

1. Delete the tables (easiest to connect the SQLite DB as a data source in PyCharm)
2. Run the Alembic migrations:
```
$ alembic revision --autogenerate
```

```
$ alembic upgrade head
```
3. Run `python project/utils/seed.py` to seed the tables 
