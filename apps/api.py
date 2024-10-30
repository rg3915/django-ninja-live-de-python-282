from ninja import NinjaAPI, Redoc


api = NinjaAPI()
# api = NinjaAPI(docs=Redoc())

api.add_router('', 'apps.core.api.router')

# Adiciona mais apps aqui
# api.add_router('', 'apps.person.api.router')
