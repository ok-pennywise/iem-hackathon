from typing import Optional
from django.conf import settings
import jwt
from ninja.security import HttpBearer

from users.models import User, UserSession


class JWTBearer(HttpBearer):
    def authenticate(self, request, token: str) -> Optional[dict]:
        try:
            payload: dict = jwt.decode(
                token, key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            try:
                UserSession.objects.get(token=token)
            except UserSession.DoesNotExist:
                return None
            return payload
        except (jwt.DecodeError, KeyError) as e:
            return None
