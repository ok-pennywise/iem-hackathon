from uuid import UUID, uuid4
from django.db import models
from django.contrib.auth.hashers import check_password

from users import managers


class User(models.Model):
    id: UUID = models.UUIDField(default=uuid4, unique=True, primary_key=True)
    email: str = models.EmailField(unique=True)

    first_name: str = models.CharField(max_length=100)
    last_name: str = models.CharField(max_length=100)

    password: str = models.CharField(max_length=128)

    objects: managers.UserManager = managers.UserManager()

    def verify_password(self, password: str) -> bool:
        return check_password(password, self.password)


class UserSession(models.Model):
    user: User = models.ForeignKey(
        User, related_name="user_sessions", on_delete=models.CASCADE
    )
    token: str = models.CharField(max_length=512)
