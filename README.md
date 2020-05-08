# Requests Site
Basically what I use for my requests.

## Setup
You will need [Poetry](https://python-poetry.org/) in order to install, after that, you can run `poetry install` 
to install all the dependencies.  
You will also need a `config.json` file with the following format:
```js
{
    "SQLALCHEMY_DATABASE_URI": "",
    "SECRET_KEY": "",
    "OSU_CLIENT_ID": 1,
    "OSU_CLIENT_SECRET": "",
    "OSU_TOKEN": ""
}
```
...and run a database migration with `flask db upgrade` command.
