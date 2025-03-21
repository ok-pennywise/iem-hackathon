from typing import TYPE_CHECKING
from django.db import models
from django.contrib.auth.hashers import make_password

if TYPE_CHECKING:
    from users.models import User


class UserManager(models.Manager):

    def create(
        self, email: str, first_name: str, last_name: str, password: str, **kw
    ) -> "User":
        user: "User" = self.model(
            email=email, first_name=first_name, last_name=last_name
        )
        user.password = make_password(password)
        user.full_clean()
        user.save()
        return user
