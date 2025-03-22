from ninja import NinjaAPI
from users import routes as user_routes
from video_generator import routes as video_generator_routes
from study_planner import routes as study_planner_routes
from mocktest import routes as mocktest_routes
from doubt_solver import routes as doubt_solver_routes

api: NinjaAPI = NinjaAPI()


api.add_router("/user/", user_routes.router)
api.add_router("/video/", video_generator_routes.router)
api.add_router("/studyplanner/", study_planner_routes.router)
api.add_router("/mocktest/", mocktest_routes.router)
api.add_router("/doubts/", doubt_solver_routes.router)
