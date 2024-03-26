install python, pipenv, docker (docker-compose).
run source by command: ```python manage.py runserver```. should be port default 8000.

we use https://www.mockaroo.com/ to create mock data.


```bash
# setup enviroment to develop
pip install pipenv
pipenv shell

pipenv install
pipenv shell

# setup database
docker compose up

# need to create migration
python manage.py makemigrations
python manage.py migrate

# create user is super
python manage.py createsuperuser
```
