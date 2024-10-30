## Criando o projeto

```bash
django-admin startproject apps .

cd apps

python ../manage.py startapp core

cd ..
```

### Configurando o projeto

Edite `settings.py`

```python
# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')

INSTALLED_APPS = [
    ...
    'django_extensions',
    'apps.core',
]
```

Edite `core/apps.py`

```python
# core/apps.py
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'  # <--
```

Rode os comandos

```bash
python contrib/env_gen.py

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

Rode a aplicação

http://localhost:8000/


## Django Ninja

### Criando uma rota

### Exemplo 1 - Único arquivo

Edite `urls.py`

```python
# urls.py
from django.contrib import admin
from django.urls import path

from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
]

api_urlpatterns = [
    path('api/v1/', api.urls),
]

urlpatterns += api_urlpatterns
```

Edite `api.py`

```python
# api.py
from http import HTTPStatus
from ninja import NinjaAPI, Router


api = NinjaAPI()

router = Router()

api.add_router('', router)


@router.get('healthcheck')
def healthcheck(request):
    return HTTPStatus.OK
```

A vantagem é que o Django Ninja já te dá o Swagger pronto.

## Redoc

Se quiser, podemos usar o Redoc, basta editar `api.py`

```python
from ninja import Redoc

api = NinjaAPI(docs=Redoc())
```

Mas vamos continuar com o Swagger. Então remova o Redoc.


### Exemplo 2 - Único arquivo com um Schema

Edite `api.py`

```python
# api.py
from http import HTTPStatus
from ninja import NinjaAPI, Router, Schema


api = NinjaAPI()

router = Router()

api.add_router('', router)


class StatusSchema(Schema):
    status: str


@router.get('healthcheck', response=StatusSchema)
def healthcheck(request):
    return HTTPStatus.OK, {'status': 'ok'}
```

# Testes

## Instalação do pytest

```bash
pip install pytest-django pytest-cov

pip freeze > requirements.txt
```

### Configurando

Edite `pytest.ini`

```
[pytest]
DJANGO_SETTINGS_MODULE = apps.settings
python_files = tests.py test_*.py *_tests.py
addopts = -p no:warnings
```


### Arquivo de teste

```bash
mkdir apps/tests

touch apps/tests/__init__.py
touch apps/tests/test_healthcheck.py
```

Edite `test_healthcheck.py`

```python
# test_healthcheck.py
from http import HTTPStatus

import pytest


@pytest.mark.django_db
def test_healthcheck(client):
    """
    Testa o endpoint healthcheck.
    Testa se retorna status_code 200.
    Testa se retorna {'status': 'ok'}
    """
    response = client.get('/api/v1/healthcheck')
    expected = {'status': 'ok'}

    assert response.status_code == HTTPStatus.OK
    assert response.json() == expected

```

### Rodando o teste

```
pytest -vv -s
```

