# Travelist.pl

Travelist Recruiting Task


## Author
[Maciej Zięba \<maciekz82@gmail.com\>](https://github.com/maciekz)


## Installation

Create a python virtualenv and activate it (Python 3.9 is recommended):

```
python -m venv venv
source ./venv/bin/activate
```

Install application and its dependencies:

```
pip install -e .
```

You can also install the application with various development tools:

```
pip install -e .[dev]
```

Run required database migrations:

```
python src/manage.py migrate
```


## Importing data from CSV file

To import data from a csv file, use the `import_users_data` command:

```
python src/manage.py import_users_data -y /path/to/file/users.csv
```

Parameter `-y` is required to confirm existing data removal.

If the import fails for some row, there will be an error message but the import will continue.


## Running application

To run the application, use the standard Django `runserver` command:

```
python src/manage.py runserver
```

When using the default port `8000`, the application is available at http://localhost:8000/payments/


## Running tests

To run tests, use the `pytest` command:

```
pytest src/payments/tests
```


## Assumptions and possible improvements to the task

To keep the task solution fairly simple, I have decided to make some decisions that possibly wouldn't be best for a real project. I have also pointed out a few possible improvements.

1. I have used Django Templates and Django Forms but a real project most probably would require creation of REST API with Django Rest Framework and a separate frontend. For the users list, currently there's no pagination, sorting or filtering.

2. The application runs locally with standard `runserver` command. A real project would require non-development WSGI server and a production configuration, possibly with dockerisation.

3. Depending on requirements, user info and user balance should be stored in separate models and not together.

4. Balance changes history is not stored and balance change reason is simply ignored.

5. I have decided not to use signals and instead to create a service function `update_user_balance()` that then runs the additional function `some_additional_function_to_run_on_balance_update()`.

6. The import command is only partially foolproof - in provided CSV there's a row with incorrect balance and it will be skipped with a message. There could be other cases that require handling, for example, the same email used twice (I assume email is unique per user).

7. I've written unit tests for the most important features but some more tests could be added.
