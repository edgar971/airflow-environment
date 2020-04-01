# Airflow 
A local Airflow environment. 

![airflow](./assets/airflow.png)
## Setup local environment
1. Download this project. 
1. Run: `make build`.

## Adding Python packages
1. Add packages to the `requirements.txt` file. 
1. Run: `make build`.
1. Restart airflow: `make start`.

## Make commands
1. `make build`: Build and download Docker images. 
1. `make start`: Starts local Docker services.
1. `make stop`: Stops Docker services.
1. `make clean`: Removes and cleans Docker container and volumes.