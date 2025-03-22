from ninja import NinjaAPI
from users import routes as user_routes
from video_generator import routes as video_generator_routes
from study_planner import routes as study_planner_routes

api: NinjaAPI = NinjaAPI()


api.add_router("/user/", user_routes.router)
api.add_router("/video/", video_generator_routes.router)
api.add_router("/studyplanner/", study_planner_routes.router)
