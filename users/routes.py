from datetime import datetime, timedelta
from typing import Optional
from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
import jwt
from ninja import Router
from django.utils import timezone

from security.authentication import JWTBearer
from users import schemas
from users.models import User, UserSession


router: Router = Router()


@router.post("/signup", response=schemas.UserOut)
def signup(request: ASGIRequest, schema: schemas.UserIn) -> User:
    return User.objects.create(**schema.dict())


@router.post("/signin")
def signin(
    request: ASGIRequest, schema: schemas.LoginRequestIn
) -> tuple[int, Optional[dict]]:
    try:
        user: User = User.objects.get(email=schema.email)
        if user.verify_password(schema.password):
            current_time: datetime = timezone.now()
            payload: dict[str, str] = {
                "id": f"{user.id}",
                "email": user.email,
                "iat": current_time,
                "exp": current_time + timedelta(days=10),
            }
            token: str = jwt.encode(payload, key=settings.SECRET_KEY, algorithm="HS256")
            UserSession.objects.create(user=user, token=token)
            return {"access_token": token}
        return 401, None
    except User.DoesNotExist:
        return 404, None


@router.post("/logout", auth=JWTBearer())
def logout(request: ASGIRequest) -> tuple[int, None]:
    try:
        user: User = User.objects.get(id=request.auth["id"])
        user.user_sessions.all().delete()
    except User.DoesNotExist:
        return 404, None


@router.get("/me", response=schemas.UserOut, auth=JWTBearer())
def current_user(request: ASGIRequest) -> tuple[int, Optional[User]]:
    try:
        return 200, User.objects.get(id=request.auth["id"])
    except User.DoesNotExist:
        return 401, None
