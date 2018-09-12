Insights Tag Service
===========================================

Dev Setup
--------------------
1. Install dependencies
```
pip install pipenv
pipenv install
```
2. Start Postgres Database
```
docker-compose up insights-tag-db
```
3. Start the server
```
pipenv run python3 tag/manage.py runserver
```
