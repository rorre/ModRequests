# Requests Site
Basically what I (and some other BNs) use for my requests.

## Setup
You will need [Poetry](https://python-poetry.org/) in order to install, after that, you can run `poetry install` 
to install all the dependencies.  
You will also need a `config.json` file with the following format:
```js
{
    "SQLALCHEMY_DATABASE_URI": "",
    "SECRET_KEY": "",
    "OSU_CLIENT_ID": ,
    "OSU_CLIENT_SECRET": "",
    "OSU_TOKEN": "",
    "DISCORD_WEBHOOKS": {
        "condition": "hook_url",
    },
    "DEFAULT_NOMINATOR": OSU_UID,
    "DOCS_ENABLED": false
}
```
...and run a database migration with `flask db upgrade` command.
