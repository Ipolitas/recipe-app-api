# recipe-app-api
# Recipe API project

## How to run
### Applications to donwload:
- Docker Desktop
- Git
- IDE

### Commands to setup project
Install requirements and build the project
`docker-compose build`
Run the server for development
`docker compose up`

### Commands to use
To run django command inside docker, the command has to be included in like so:
`docker-compose run --rm app sh -c "python manage.py my_command"`

### Useful commands:
Run tests:
`docker-compose run --rm app sh -c "pytest"`
Run lint:
`docker-compose run --rm app sh -c "flake8"`
Run both
`docker-compose run --rm app sh -c "pytest && flake8"`
Make migration:
`docker-compose run --rm app sh -c "XXXXXXXX"`
