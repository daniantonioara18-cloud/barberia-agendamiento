from django.core.management.base import BaseCommand
from Barberia.models import Dias, Horas, Tipo_servicio

class Command(BaseCommand):
    help = "Carga datos iniciales: días, horas y servicios (BASE + ADDON)"

    def handle(self, *args, **options):

        # 1) DÍAS
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        for d in dias:
            Dias.objects.get_or_create(dia_Dias=d)

        # 2) HORAS
        horas = set()

        def agregar_rango(h_inicio, h_fin, incluye_media_hora_final=True):
            h = h_inicio
            m = 0
            while True:
                horas.add(f"{h:02d}:{m:02d}")

                # Condición de corte
                if h == h_fin and ((m == 30 and incluye_media_hora_final) or (m == 0 and not incluye_media_hora_final)):
                    break

                m += 30
                if m >= 60:
                    m = 0
                    h += 1

        # Lun–Vie: 12:00 a 19:30  (=> h_fin=19, incluye 19:30)
        agregar_rango(12, 19, incluye_media_hora_final=True)

        # Sáb: 12:00 a 15:00 (=> h_fin=15, NO incluye 15:30)
        agregar_rango(12, 15, incluye_media_hora_final=False)

        for hora in sorted(horas):
            Horas.objects.get_or_create(hora_Horas=hora)

        # 3️⃣ SERVICIOS (BASE y ADDON)
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

        self.stdout.write(self.style.SUCCESS("Seed ejecutado correctamente."))