from ninja import ModelSchema, Schema

from users.models import User


class UserIn(ModelSchema):
    class Meta:
        model: type[User] = User
        fields: tuple[str] = ("email", "first_name", "last_name", "password")


class UserOut(ModelSchema):
    class Meta:
        model: type[User] = User
        fields: tuple[str] = ("id", "email", "first_name", "last_name")


class LoginRequestIn(Schema):
    email: str
    password: str


class PasswordChangeIn(Schema):
    current_password: str
    new_password: str
