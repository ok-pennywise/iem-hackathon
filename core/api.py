from ninja import NinjaAPI
from users import routes as user_routes
from video_generator import routes as video_generator_routes

api: NinjaAPI = NinjaAPI()


api.add_router("/user/", user_routes.router)
api.add_router("/video/", video_generator_routes.router)
