## How to run
### Applications to download:
- Docker Desktop
- Git
- IDE

### Commands to setup project
- Install requirements and build the project
```docker-compose build```
- Run the server for development
```docker compose up```

### Commands to use
To run django command inside docker, the command has to be included in like so:<br />
```docker-compose run --rm app sh -c "python manage.py my_command"```

### Useful commands:
- Run tests:
```docker-compose run --rm app sh -c "pytest"```
- Run lint:
```docker-compose run --rm app sh -c "flake8"```
- Run both:
```docker-compose run --rm app sh -c "pytest && flake8"```
- Make migrations:
```docker-compose run --rm app sh -c "python manage.py makemigrations"```
- Apply migrations:
```docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py migrate"```
- Clear the volume (wipe the local database):
```docker volume ls``` - to list all volumes<br />
```docker-compose down``` - to clear any container that would be using volume<br />
```docker volume rm recipe-app-api_dev-db-data``` - removes the volume
