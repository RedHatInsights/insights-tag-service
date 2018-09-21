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
pipenv run python3 app.py
```
