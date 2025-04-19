```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

python manage.py create_test_users

poetry run python manage.py create_test_users
poetry run python manage.py test_optimization
poetry run python manage.py test_dependancies
poetry run python manage.py setup_schedules


poetry run coverage run --source='.' manage.py test
poetry run coverage run --source='.' manage.py test api_v1.tests.test_category
poetry run coverage xml
```

```
poetry run python manage.py tailwind install
poetry run python manage.py tailwind start
```
