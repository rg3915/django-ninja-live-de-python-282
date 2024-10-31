from http import HTTPStatus
from ninja import Query, Router
from ninja.pagination import paginate

from django.contrib.auth.models import User

from .models import Task
from .schemas import StatusSchema, UserSchema, UserSimpleSchema, UserWithGroupSchema, TaskSchema, TaskFilterSchema  # noqa F401


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


@router.get('users', response=list[UserWithGroupSchema])
def list_users(request):
    return User.objects.all()


@router.get('tasks', response=list[TaskSchema], tags=['Tasks'])
@paginate
def list_tasks(request, filters: TaskFilterSchema = Query(...)):
    tasks = Task.objects.all()
    return filters.filter(tasks)
