from django.core.management.base import BaseCommand
from Barberia.models import Tipo_servicio

class Command(BaseCommand):
    help = "Crea/actualiza servicios BASE y ADDON de Erik"

    def handle(self, *args, **options):
        servicios = [
            # BASE
            ("Corte de pelo", 8000, "BASE"),
            ("Limpieza facial", 10000, "BASE"),

            # ADDON
            ("Perfilado de barba", 3000, "ADDON"),
            ("Perfilado de cejas", 2000, "ADDON"),
            ("Líneas", 1000, "ADDON"),
        ]

        for nombre, precio, tipo in servicios:
            obj, created = Tipo_servicio.objects.update_or_create(
                nombre=nombre,
                defaults={"precio_servicio": precio, "tipo": tipo},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Creado: {nombre} ({tipo})"))
            else:
                self.stdout.write(self.style.WARNING(f"Actualizado: {nombre} ({tipo})"))

        self.stdout.write(self.style.SUCCESS("Seed de servicios OK."))
