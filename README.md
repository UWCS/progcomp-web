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

Once the server is running, you control it by running the scripts in `/progcomp/scripts` from a separate terminal. First run `pipenv shell` to avoid prefixing each command with `pipenv run`.

> 1. Create a progcomp and set its dates
```sh
python progcomp/scripts/create_progcomp.py <progcomp_name>
export SCRIPT_PROGCOMP="<progcomp_name>"      # Future scripts reference this env var
python progcomp/scripts/set_pg_start_time.py "in 5 mins"   # This parsing is flexible
python progcomp/scripts/set_pg_start_time.py "8pm"   # This parsing is flexible
```

> 2. Input problems into directory `/problems/<progcomp_name>`
Structure should be

```text
problems
├───<progcomp_name>
│   │   problems.pdf
│   ├───<problem_one>
│   │   ├───input
│   │   │       <0-test>.txt
│   │   │       <1-test>.txt
│   │   │       ...
│   │   └───output
│   │           <0-test>.txt
│   │           <1-test>.txt
│   │           ...
│   ├───<problem_two>
│   │   ├───input
│   .   │       ...
│   .   └───output
│   .           ...
│
├───<other_progcomp>
│   ...

```

> 3. Sync problems into DB, then set to visible
- Open: Visible and submissions allowed
- Closed: Visible but no submissions allowed
- Hidden: Not visible and no submissions
- To allow fine-grained control, we set problem and progcomp separately
    - Problem inherits visibility from progcomp if more restrictive than problem
    - e.g. If problem is closed, but progcomp is hidden, problems will be hidden,
    - If you then switched the progcomp to open, the problem would be closed.
- By default, the leaderboards are hidden, use `toggle_pg_leaderboard.py` to change.
```sh
python progcomp/scripts/update_pg_problems.py   # Read from directory
python progcomp/scripts/get_problems.py         # List results
# Set visibility for each problem - can reveal one-by-one during competition
python progcomp/scripts/set_problem_visibility.py <problem_one> <open|closed|hidden>
python progcomp/scripts/set_problem_visibility.py <problem_two> <open|closed|hidden>
...

# Set visibility for progcomp once ready
python progcomp/scripts/set_pg_visibility.py <open|closed|hidden>
```

> 4. Switch out problem PDF while live
- As more problems are revealed, you need to update the PDF as well:
```sh
python progcomp/scripts/swap_pg_pdf.py <new_pdf_path>
# Moves old PDF to __problems_old.pdf in case you need to undo
# Copies new into problems.pdf
```

> 5. Query information while live
- If you want a full dump of info that isn't restricted to what is visible on the website, use the get scripts:
```sh
python progcomp/scripts/get_problems.py     # List all problems from all progcomps
python progcomp/scripts/get_scores.py <problem> <test>  # Get scores for a specific problem
python progcomp/scripts/get_scores_overall.py   # Get overall leaderboard
python progcomp/scripts/get_submissions.py      # List all submissions
```

> 6. Custom behaviour
- SQL-Alchemy makes editing the data while live very easy, write your queries following the template and you can do a lot
- Alembic is used for DB versioning, if you want to add or remove fields (don't remove while live)