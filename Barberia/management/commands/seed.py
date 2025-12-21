from django.core.management.base import BaseCommand
from Barberia.models import Dias, Horas, Tipo_servicio, Horario

class Command(BaseCommand):
    help = "Seed completo: días, horas, servicios BASE/ADDON + migración segura"

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
                if h == h_fin and ((m == 30 and incluye_media_hora_final) or (m == 0 and not incluye_media_hora_final)):
                    break
                m += 30
                if m >= 60:
                    m = 0
                    h += 1

        agregar_rango(12, 19, True)   # Lun–Vie
        agregar_rango(12, 15, False)  # Sábado

        for h in sorted(horas):
            Horas.objects.get_or_create(hora_Horas=h)

        # 3) SERVICIOS NUEVOS
        servicios = [
            ("Corte de pelo", 8000, "BASE"),
            ("Limpieza facial", 10000, "BASE"),
            ("Perfilado de barba", 3000, "ADDON"),
            ("Perfilado de cejas", 2000, "ADDON"),
            ("Líneas", 1000, "ADDON"),
        ]

        for nombre, precio, tipo in servicios:
            Tipo_servicio.objects.update_or_create(
                nombre=nombre,
                defaults={"precio_servicio": precio, "tipo": tipo},
            )

        # 4) MIGRACIÓN SEGURA (clave)
        mapa = {
            "Corte": "Corte de pelo",
            "Corte + Barba": "Corte de pelo",
            "Barba": "Perfilado de barba",
        }

        for viejo, nuevo in mapa.items():
            try:
                s_viejo = Tipo_servicio.objects.get(nombre=viejo)
                s_nuevo = Tipo_servicio.objects.get(nombre=nuevo)
            except Tipo_servicio.DoesNotExist:
                continue

            Horario.objects.filter(Tipo_servicio=s_viejo).update(Tipo_servicio=s_nuevo)

        # 5) LIMPIEZA FINAL
        Tipo_servicio.objects.filter(nombre__in=mapa.keys()).delete()

        self.stdout.write(self.style.SUCCESS("Seed completo ejecutado correctamente."))