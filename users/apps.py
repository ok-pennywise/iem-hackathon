from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "users"

    def ready(self) -> None:
        from users import signals

        return super().ready()
