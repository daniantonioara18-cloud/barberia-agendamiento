import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Crea superusuario para Erik si no existe"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.environ.get("ERIK_ADMIN_USER", "erik")
        password = os.environ.get("ERIK_ADMIN_PASSWORD")
        email = os.environ.get("ERIK_ADMIN_EMAIL", "")

        if not password:
            self.stdout.write(self.style.ERROR("Falta ERIK_ADMIN_PASSWORD"))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("El superusuario ya existe"))
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

        self.stdout.write(self.style.SUCCESS("Superusuario Erik creado correctamente"))
