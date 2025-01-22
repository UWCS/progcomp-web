![UWCS Challenge Logo](progcomp/static/challenge_logo.svg)

## Setup Instructions

> 1. First, install the `pipenv` package, by using this command in the terminal:

```sh
pip install pipenv
```

> 2. Then, we use `pipenv` to read the contents of the Pipfile and install all the necessary packages that make the frontend work. This can be accompished with:

```sh
pipenv install
```

(Make sure the terminal is opened within the correct folder!)

> 3. Initialize the database:

```sh
pipenv run python progcomp/scripts/initialize.py
```

> 4. Run the server with:

```sh
pipenv run flask --app progcomp --debug run
```

The site will then be running locally at `localhost:5000`, and you can access it as a url in your preferred web browser.

You can stop it at any time by pressing **CTRL+C** in the terminal.

# Admin Operation

Once the server is running, you control it by using the admin panel, found at `localhost:5000/admin`. The password used is an set using environment variables.

## Custom behaviour
- SQL-Alchemy makes editing the data while live very easy, write your queries following the template and you can do a lot
- Alembic is used for DB versioning, if you want to add or remove fields (don't remove while live)