from http import HTTPStatus
from ninja import NinjaAPI, Redoc, Router, Schema


api = NinjaAPI()
# api = NinjaAPI(docs=Redoc())

router = Router()

api.add_router('', router)


class StatusSchema(Schema):
    status: str


@router.get('healthcheck', response=StatusSchema)
def healthcheck(request):
    return HTTPStatus.OK, {'status': 'ok'}
