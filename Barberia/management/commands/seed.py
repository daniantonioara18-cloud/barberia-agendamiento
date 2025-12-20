from django.core.management.base import BaseCommand
from Barberia.models import Dias, Horas, Tipo_servicio

class Command(BaseCommand):
    help = "Carga datos iniciales: días, horas y servicios"

    def handle(self, *args, **options):

        # 1️⃣ DÍAS
        dias = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
        ]

        for d in dias:
            Dias.objects.get_or_create(dia_Dias=d)

        # 2️⃣ HORAS
        # Lunes a Viernes: 12:00 a 19:30
        # Sábado: 12:00 a 15:00
        horas = set()

        def generar_horas(h_inicio, h_fin):
            h = h_inicio
            m = 0
            while True:
                horas.add(f"{h:02d}:{m:02d}")
                if h == h_fin and m == 30:
                    break
                m += 30
                if m >= 60:
                    m = 0
                    h += 1

        # Lunes a Viernes
        generar_horas(12, 19)

        # Sábado (hasta 15:00)
        h = 12
        m = 0
        while True:
            horas.add(f"{h:02d}:{m:02d}")
            if h == 15 and m == 0:
                break
            m += 30
            if m >= 60:
                m = 0
                h += 1

        for hora in sorted(horas):
            Horas.objects.get_or_create(hora_Horas=hora)

        # 3️⃣ SERVICIOS (EDITABLES POR TI)
        servicios = [
            ("Corte", 8000),
            ("Corte + Barba", 15000),
            ("Barba", 5000),
        ]

        for nombre, precio in servicios:
            obj, created = Tipo_servicio.objects.get_or_create(
                nombre=nombre,
                defaults={"precio_servicio": precio}
            )

            # Si ya existe, actualiza el precio
            if not created and obj.precio_servicio != precio:
                obj.precio_servicio = precio
                obj.save(update_fields=["precio_servicio"])

        self.stdout.write(self.style.SUCCESS("Seed ejecutado correctamente."))
