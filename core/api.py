from ninja import NinjaAPI
from users import routes

api: NinjaAPI = NinjaAPI()


api.add_router("/user/", routes.router)
