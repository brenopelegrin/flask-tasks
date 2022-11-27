# flask-tasks

This is a generic Flask RESTful API written in Python that can receive task requests with some arguments, run some logic with the arguments provided and store the results on a SQL database. The results can then be retrieved from the API.

:warning: **This repository might be outdated in terms of features and fixes. For more frequent and recent updates, please check the [flask-tasks-docker](https://github.com/brenopelegrin/flask-tasks-docker) repository** 

## Main features

- You can setup multiple task handlers that can **proccess tasks in parallel**
- **Highly customizable** to fulfill your needs
- You can setup multiple janitors that can clean up the database in parallel
- Can receive task from ```POST``` request **passing multiple parameters** in ```json```
- Can store the received tasks in a SQL database and **do some computation** with them
- Can return the result of the task from ```GET``` request passing the task ID as parameter

## :rocket: Getting started

- In what applications should I use it?
  
    You should use the ```flask-tasks``` when you need a server to do some computation based on received arguments and store the results of the computation for later visualization

### :gear: Setting up the environment

First, make sure you have ```python3```, ```pip3``` and ```virtualenv``` installed.

Then, clone the repository and go to the cloned directory:
```bash
git clone https://github.com/brenopelegrin/flask-tasks.git && cd flask-tasks
```
Activate the python virtual environment:
```bash
source bin/activate
```

Then, install all requirements by running:
```bash
pip install -r requirements.txt
```

Finally, setup the environment variables on the ```.env``` file:
```bash
DATABASE_URL=postgres://[user]:[password]@[database_server_ip]:[port]/[database_name]
BACKEND_URL=https://[backend_server_ip]:[port]
FRONTEND_URL=https://[frontend_server_ip]:[port]
MAX_TASK_TIME=[time_in_seconds]
```
The ```BACKEND_URL``` and ```FRONTEND_URL``` variables need to be defined for CORS to work if you need communication between front-end and back-end in JavaScript.

The ```MAX_TASK_TIME``` variables defines the maximum time of permanency of data in the database (in seconds)

### Running locally with Heroku CLI

The app is ready to run with Heroku CLI. Just configure the number of handlers and janitors as you want and then run the following

```
heroku local
```

### Customizing the number of handlers and janitors

On the ```Procfile```, add as much handlers and janitors as you want, for example:

```
web: gunicorn app:app -c gunicorn.conf.py
handler1: python handler.py
handler2: python handler.py
handler3: python handler.py
janitor1: python janitor.py
janitor2: python janitor.py
janitor3: python janitor.py
```

### Running manually

First, you will need to export all the environment variables in the ```.env```file:

```bash
export DATABASE_URL=postgres://[user]:[password]@[database_server_ip]:[port]/[database_name]
export BACKEND_URL=https://[backend_server_ip]:[port]
export FRONTEND_URL=https://[frontend_server_ip]:[port]
export MAX_TASK_TIME=[time_in_seconds]
```

Then, in separate terminals, run the commands to start ```gunicorn``` and as many instances of ```handler```and ```janitor``` as you want.

```bash
gunicorn app:app -c gunicorn.conf.py
```

```
python handler.py
```

```
python janitor.py
```

## API endpoints

### /task/new

Method: ```POST```

This endpoint will register a new task in the server, passing some arguments in ```application/json``` format and returning the task info in ```application/json``` format:

Example of request:

Parameters:
```json
{
    "required_arg":"test"
}
```

```bash
curl -X POST localhost:5000/task/new -H 'Content-Type: application/json' -d '{"required_arg":"test"}'
```

Example of response:

```json
{
"id": 192,
"result": null,
"args": {"required_arg": "test"},
"status": "waiting",
"expire": 1668797956,
"required_arg": "test",
"created": 1668797946
}
```

### /task/```<task_id>```/view

Method: ```GET```

This endpoint will return the current data for the task with id ```task_id``` in ```application/json``` format:

Example of request:

Parameters: ```<task_id>```

```bash
curl -X GET localhost:5000/task/1/view
```

Example of response:

```json
{
"id": 1,
"result": {"message": "some_message"},
"args": {"required_arg": "test"},
"status": "done",
"expire": 1668797956,
"required_arg": "test",
"created": 1668797946
}
```

The status of a retrieved task can be:
- ```waiting```
  
  Means that the task has been registered but has not yet been computed
- ```running```
  
  Means that the task has been registered and is actually being computed
- ```done```
  
  Means that the task has been registered and have already been computed

## The ```handler```

The handler is a module of the system that will scan through the database and get the tasks with ```waiting``` status.

Then, it will run the ```ExecuteWhenRunningTask(task_id, args)``` function which should return a result for the task. After that, the result is stored in the ```result``` key of the task in the database. This function can be customized to fulfill your needs.

The handler will mark the current task row as locked in the database, so that the other instances of handlers can't edit at the same time.

## The ```janitor```
The janitor is a module of the system that will scan through the database and get the tasks that exceeded the maximum data permanency time (```MAX_TASK_TIME``` variable) in the database.

Then, it will delete the task from the database. The janitor will mark the current task row as locked in the database, so that the other instances of handlers can't edit at the same time. 
