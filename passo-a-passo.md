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


## Request e Response

### Request

O **Request** é a requisição, ou solicitação, que o cliente faz ao servidor para acessar um recurso. A requisição geralmente inclui:

* **Método HTTP:** Define o tipo de requisição:
    * GET - obter dados
    * POST - criar dados
    * PUT - atualizar dados
    * PATCH - atualizar dados parcialmente
    * DELETE - excluir dados

* **URL:** Define o endpoint específico da API que está sendo acessado.

* **Headers:** Podem conter informações adicionais, como autenticação e tipo de conteúdo (ex.: JSON).

* **Body** (Corpo da Requisição): Contém os dados que são enviados, geralmente no formato JSON, e é usado especialmente em requisições `POST` e `PUT` para enviar informações ao servidor.

### Response

A **Response** é a **resposta** que o servidor retorna para o cliente após processar a requisição. Esse retorno contém informações como:

* **Status Code:** Informa se a operação foi bem-sucedida (ex.: 200 para sucesso, 201 para criação, 404 para não encontrado, etc.).

https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status

* **Headers:** Incluem informações sobre o tipo de conteúdo da resposta, cache, etc.

* **Body** (Corpo da Resposta): Os dados que o cliente vai receber, geralmente em formato JSON.


```python
# api.py
...

@router.get('add')
def add(request, a: int, b: int):
    return {'result': a + b}
```


### Exemplo 2 - Único arquivo com um Schema

Então, podemos definir nossas próprias respostas. Para isso vamos usar Schema.

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

## Parâmetros Operacionais

* tags
* summary
* description

```python
# api.py
@router.get(
    'healthcheck',
    response=StatusSchema,
    tags=['Health Check'],
    summary='Health Check',
    description='Verificação de status que permite monitorar a saúde da API.'
)
def healthcheck(request):
    return HTTPStatus.OK, {'status': 'ok'}


@router.get('add')
def add(request, a: int, b: int):
    """
    Envie dois números inteiros:
    - a
    - b
    """
    return {'result': a + b}
```

## Separando as APIs

#### Deletando alguns arquivos

```bash
rm -f apps/core/tests.py
rm -f apps/core/views.py
```

#### Criando outros arquivos

Crie core/api.py
E core/schemas.py

```bash
touch apps/core/api.py
touch apps/core/schemas.py
```

```
tree

.
├── apps
│   ├── core
│   │   ├── api.py  # <---
│   │   └── schemas.py
│   ├── api.py  # <-------
│   ├── settings.py
│   ├── urls.py
```

Edite `apps/api.py`

```python
# apps/api.py
from ninja import NinjaAPI, Redoc


api = NinjaAPI()
# api = NinjaAPI(docs=Redoc())

api.add_router('', 'apps.core.api.router')

# Adiciona mais apps aqui
# api.add_router('', 'apps.person.api.router')
```

Edite `apps/core/api.py`

```python
# apps/core/api.py
from http import HTTPStatus
from ninja import Router

from .schemas import StatusSchema


router = Router(tags=['Core'])


@router.get(
    'healthcheck',
    response=StatusSchema,
    tags=['Health Check'],
    summary='Health Check',
    description='Verificação de status que permite monitorar a saúde da API.'
)
def healthcheck(request):
    return HTTPStatus.OK, {'status': 'ok'}


@router.get('add')
def add(request, a: int, b: int):
    """
    Envie dois números inteiros:
    - a
    - b
    """
    return {'result': a + b}
```

Repare que podemos adicionar uma tag geral para a app.

```python
router = Router(tags=['Core'])
```


Edite `apps/core/schemas.py`

```python
# apps/core/schemas.py
from ninja import Schema


class StatusSchema(Schema):
    status: str
```


> Rode os testes novamente.

```
pytest -vv
```

## Definindo Schemas

### ModelSchema

O [ModelSchema](https://django-ninja.dev/guides/response/django-pydantic/#modelschema) gera o schema automaticamente a partir do modelo.

Edite `core/api.py`

```python
# core/api.py
from django.contrib.auth.models import User

from .schemas import UserSchema


@router.get('users', response=list[UserSchema])
def list_users(request):
    return User.objects.all()
```

Edite `core/schemas.py`

```python
# core/schemas.py
from ninja import ModelSchema, Schema

from django.contrib.auth.models import User


class UserSchema(ModelSchema):

    class Meta:
        model = User
        fields = '__all__'
```

Mas aqui nós temos uma falha grave: `__all__`

[Using ALL model fields](https://django-ninja.dev/guides/response/django-pydantic/#using-all-model-fields)

> Mostrar como é retornado na API.

#### Exclude

```python
# core/schemas.py
class UserSchema(ModelSchema):

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'date_joined', 'user_permissions', 'groups']
```



### Nested Schemas

Esquemas Aninhados

Edite `core/models.py`

```python
# core/models.py
from django.db import models


class Task(models.Model):
    title = models.CharField('título', max_length=100)
    is_completed = models.BooleanField('completo', default=False)
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('pk',)
        verbose_name = 'tarefa'
        verbose_name_plural = 'tarefas'

    def __str__(self):
        return f'{self.title}'
```

Edite `core/admin.py`

```python
# core/admin.py
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_completed', 'user__first_name', 'user__last_name')
    search_fields = ('title',)
```

Rode os comandos

```bash
python manage.py makemigrations
python manage.py migrate
```

Vamos adicionar dados pelo shell_plus.

```python
user = User.objects.first()

titles = [
    'Estudar Python',
    'Estudar Django',
    'Estudar Django Ninja',
]

for title in titles:
    Task.objects.create(title=title, user=user)

# E vamos criar uma sem User.
Task.objects.create(title='Convidado para a próxima Live')
```


Edite `core/api.py`

```python
# core/api.py
from .models import Task
from .schemas import TaskSchema


@router.get('tasks', response=list[TaskSchema], tags=['Tasks'])
def list_tasks(request):
    return Task.objects.all()
```

Edite `core/schemas.py`

```python
# core/schemas.py
from .models import Task


class TaskSchema(ModelSchema):

    class Meta:
        model = Task
        fields = ['id', 'title', 'is_completed', 'user']
```

> Ver o resultado no Swagger.

#### Usando os Esquemas Aninhados.

Edite `core/schemas.py`

```python
# core/schemas.py
class TaskSchema(ModelSchema):
    user: UserSchema

    class Meta:
        model = Task
        fields = ['id', 'title', 'is_completed']
```

### create_schema

Edite `core/schemas.py`

```python
# core/schemas.py
from ninja.orm import create_schema

UserSimpleSchema = create_schema(
    User,
    fields=['id', 'username', 'first_name', 'last_name']
)
```

Edite `core/api.py`

```python
# core/api.py
from .schemas import UserSimpleSchema


@router.get('users', response=list[UserSimpleSchema])
def list_users(request):
    return User.objects.all()
```

### depth

Retorna os dados de uma ForeignKey, OneToOne, ManyToMany.

Edite `core/api.py`

```python
# core/api.py
from .schemas import UserWithGroupSchema


@router.get('users', response=list[UserWithGroupSchema])
def list_users(request):
    return User.objects.all()
```


Edite `core/schemas.py`

```python
# core/schemas.py
UserWithGroupSchema = create_schema(
    User,
    depth=1,
    fields=['id', 'username', 'first_name', 'last_name', 'groups']
)
```

### custom_fields on create_schema

Edite `core/schemas.py`

```python
# core/schemas.py
UserWithGroupSchema = create_schema(
    User,
    depth=1,
    fields=['id', 'username', 'first_name', 'last_name', 'groups'],
    custom_fields=[
        ('get_full_name', str, None)
    ]
)
```

Github: [get_full_name](https://github.com/django/django/blob/main/django/contrib/auth/models.py#L493)


### Field and alias

> Deixe uma task sem user.

> Acesse `/api/v1/tasks` .


Edite `core/schemas.py`

```python
# core/schemas.py
class UserSchema(ModelSchema):
    full_name: str = Field(None, alias='get_full_name')
    username: str = Field(None)

    class Meta:
        model = User
        exclude = ['password', 'last_login', 'date_joined', 'user_permissions', 'groups']
```

### Resolve

Edite `core/models.py`

```python
# core/models.py

class StatusChoices(models.TextChoices):
    CANCELADO = 'C', 'Cancelado'
    PENDENTE = 'P', 'Pendente'
    FINALIZADO = 'F', 'Finalizado'


class Task(models.Model):
    ...
    status = models.CharField(
        max_length=1,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE,
    )
```

Rode os comandos

```bash
python manage.py makemigrations
python manage.py migrate
```

Edite `core/schemas.py`

```python
# core/schemas.py
class TaskSchema(ModelSchema):
    user: UserSchema
    status_display: str

    class Meta:
        model = Task
        fields = ['id', 'title', 'is_completed', 'status']

    @staticmethod
    def resolve_status_display(obj):
        return obj.get_status_display()
```


## Paginação

O padrão é o LimitOffsetPagination.

Edite `core/api.py`

```python
# core/api.py
from ninja.pagination import paginate

@router.get('tasks', response=list[TaskSchema], tags=['Tasks'])
@paginate
def list_tasks(request):
    return Task.objects.all()
```

> Postman

http://localhost:8000/api/v1/tasks?limit=2&offset=0

http://localhost:8000/api/v1/tasks?limit=2&offset=2

[pagination](https://django-ninja.dev/guides/response/pagination/)

## Campo de Busca

Edite `core/schemas.py`

```python
# core/schemas.py
from ninja import FilterSchema
from typing import Optional

class TaskFilterSchema(FilterSchema):
    title: Optional[str] = Field(None, q='title__icontains')
```

Edite `core/api.py`

```python
# core/api.py
from ninja import Query

from .schemas import TaskFilterSchema


@router.get('tasks', response=list[TaskSchema], tags=['Tasks'])
@paginate
def list_tasks(request, filters: TaskFilterSchema = Query(...)):
    tasks = Task.objects.all()
    return filters.filter(tasks)
```


## CRUD

Assista meu [video sobre CRUD](https://youtu.be/CRt5DeXWJdQ?si=dLjEdneBycrua3OP).

E leia a doc em [CRUD example](https://django-ninja.dev/tutorial/other/crud/).

## Django Ninja Extra e Django Ninja JWT

[django-ninja-extra](https://eadwincode.github.io/django-ninja-extra/)

[django-ninja-jwt](https://eadwincode.github.io/django-ninja-jwt/)

