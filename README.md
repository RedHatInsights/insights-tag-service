Insights Tag Service
===========================================

Dev Setup
--------------------
1. Install dependencies
```
pip install pipenv alembic --user
pipenv install
```

2. Start Postgres Database (might need to run this as root depending on your docker setup)
```
docker-compose up insights-tag-db
```

3. Migrate the Database
```
pipenv shell
PYTHONPATH=. alembic upgrade head
```

4. Start the server
```
pipenv run server
```

Testing
--------------------
1. Install dependencies
```
pip install pipenv alembic --user
pipenv install
npm install oatts mocha chakram -g
```

2. Run generated tests
```
pipenv run test
```
