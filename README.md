# quicksets
[![Build Status](https://travis-ci.org/ihor-nahuliak/quicksets.svg?branch=master)](https://travis-ci.org/ihor-nahuliak/quicksets)
[![Coverage Status](https://coveralls.io/repos/github/ihor-nahuliak/quicksets/badge.svg)](https://coveralls.io/github/ihor-nahuliak/quicksets)

Lightweight settings library based on Python classes. No dependency!


#### Use inherited settings classes
Rewrite just attributes that you really need to change:

File: `myapp.settings.develop.py`
```python
class DevelopConfig:
    POSTGRESQL_HOST = 'localhost'
    POSTGRESQL_PORT = 5432
    POSTGRESQL_USERNAME = 'postgres'
    POSTGRESQL_PASSWORD = None
    POSTGRESQL_DATABASE = 'db'
    POSTGRESQL_POOL_MIN_SIZE = 4
    POSTGRESQL_POOL_MAX_SIZE = 32
    POSTGRESQL_POOL_RECYCLE = True

    @property
    def POSTGRESQL_CONNECTION_OPTIONS(self):
        return {
            'user': self.POSTGRESQL_USERNAME,
            'password': self.POSTGRESQL_PASSWORD,
            'host': self.POSTGRESQL_HOST,
            'port': self.POSTGRESQL_PORT,
            'database': self.POSTGRESQL_DATABASE,
            'minsize': self.POSTGRESQL_POOL_MIN_SIZE,
            'maxsize': self.POSTGRESQL_POOL_MAX_SIZE,
            'pool_recycle': self.POSTGRESQL_POOL_RECYCLE
        }
```

File: `myapp.settings.testing.py`
```python
from myapp.settings.develop import DevelopConfig

class TestingConfig(DevelopConfig):
    POSTGRESQL_DATABASE = 'db_test'
```

File: `myapp.settings.product.py`
```
from myapp.settings.develop import DevelopConfig

class ProductConfig(DevelopConfig):
    POSTGRESQL_HOST = '10.0.0.1'
    POSTGRESQL_DATABASE = 'db_prod'
    POSTGRESQL_USERNAME = 'prod_user'
    POSTGRESQL_PASSWORD = '?????????'
```

Now you can chose your config just setting up env variable:
```bash
export SETTINGS="myapp.settings.product"
```


#### Use quicksets with Flask

File: `myapp.application.py`
```python
from flask import Flask
from quicksets import settings

app = Flask(__name__)
app.config.from_object(settings)
```


#### Use quicksets with aiohttp

File: `myapp.application.py`
```python
from aiohttp import web
from quicksets import settings

from myapp.middlewares import middlewares
from myapp.views import routes


async def create_app():
    app = web.Application(middlewares=middlewares)
    app.add_routes(routes)
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host=settings.HOST, port=settings.PORT)
```
