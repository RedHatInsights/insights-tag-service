Insights Tag Service
===========================================

Dev Setup

--------------------

1. Install dependencies

``` sh
pip install pipenv alembic --user
pipenv install
```

2. Start Postgres Database (might need to run this as root depending on your docker setup)

``` sh
docker-compose up insights-tag-db
```

3. Migrate the Database

``` sh
pipenv shell
PYTHONPATH=. alembic upgrade head
```

4. Start the server

``` sh
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

Dev Guidelines

--------------------

- In general exceptions should be handled via app.add_error_handler. See [here](https://connexion.readthedocs.io/en/latest/exceptions.html#rendering-exceptions-through-the-flask-handler)
- Follow these steps to generate a new migration
  1. Start a virtual env

  ``` sh
  pipenv shell
  ```

  2. Update database to current version

  ``` sh
  PYTHONPATH=. alembic upgrade head
  ```

  3. Generate new migration version from changes to db.models

  ``` sh
  PYTHONPATH=. alembic revision --autogenerate -m "Description of model changes"
  ```

  4. Open db/migrations/versions/{new-script}.py and make any required manual changes
  5. Run the migration

  ``` sh
  PYTHONPATH=. alembic upgrade head
  ```
