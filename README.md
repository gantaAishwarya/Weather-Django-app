# Weather-Django-app

The security of your IT infrastructure is important to us.

- Documentation: [Swagger Docs](http://127.0.0.1:8000/docs/) or [Re-Doc](http://127.0.0.1:8000/redoc/)


## Installation - Docker

The easiest way to get up and running is with [Docker](https://www.docker.com/).

Just [install Docker](https://www.docker.com/get-started) and
[Docker Compose](https://docs.docker.com/compose/install/)

This will spin up a PostgreSQL database, Web backend, and also run your migrations.

You can then go to [localhost:8000](http://localhost:8000/) to view the app.

*Note: if you get an error, make sure you have a `.env` file, or create one based on `.env.example`.*


## Installation - Native

You can also install/run the app directly on your OS using the instructions below.

Setup a virtual environment and install requirements
(this example uses [virtualenv](https://virtualenv.pypa.io/en/latest/user_guide.html)):

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements/local.txt
```

## Set up database

*If you are using Docker you can skip these steps.*

Create a database named `ch_demo_db`.

```
createdb ch_demo_db
```

Create database migrations:

```
./manage.py makemigrations
```

Create database tables:

```
./manage.py migrate
```

## Running server

**Docker:**

```bash
make start
```

**Native:**

```bash
./manage.py runserver
```

## Running Tests

To run tests:

**Docker:**

```bash
make test
```

**Native:**
```bash
python manage.py test
```