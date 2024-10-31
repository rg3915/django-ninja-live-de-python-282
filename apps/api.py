from ninja import NinjaAPI, Redoc  # noqa F401


api = NinjaAPI()
# api = NinjaAPI(docs=Redoc())

api.add_router('', 'apps.core.api.router')

# Adiciona mais apps aqui
# api.add_router('', 'apps.person.api.router')
