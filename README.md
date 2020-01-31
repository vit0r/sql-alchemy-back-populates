# Usage

## Result from sqllite databse

```shell
sqlitebrowser database.db
python -i one-to-one.py
```

## Result from postgresql databse

```shell
docker run --name local-postgres -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 postgres
python -i one-to-one-pgsql.py
docker exec -it local-postgres psql -U postgres
```
