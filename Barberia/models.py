from django.db import models
from django.core.exceptions import ValidationError  # NUEVO
from .utils import validar_rut, formatear_rut       # NUEVO

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    celular = models.CharField(max_length=12)
    rut = models.CharField(max_length=12)

    def clean(self):
        # Validar RUT real
        if not validar_rut(self.rut):
            raise ValidationError({"rut": "El RUT ingresado no es válido."})

        # Formatear RUT con puntos y guion
        self.rut = formatear_rut(self.rut)

        # Normalizar celular a +569*******
        tel = self.celular.replace(" ", "")
        # Si ya viene con +569 lo dejamos igual
        if not tel.startswith("+569"):
            # 9*******  -> +569*******
            if tel.startswith("9") and len(tel) == 9:
                tel = "+56" + tel
            # 569******* -> +569*******
            elif tel.startswith("569") and len(tel) == 11:
                tel = "+" + tel
            # Cualquier otra cosa, forzamos +569 delante
            else:
                if tel.startswith("+56"):
                    tel = "+569" + tel[-8:]
                else:
                    tel = "+569" + tel[-8:]

        self.celular = tel

    def save(self, *args, **kwargs):
        # Llamamos a clean() antes de guardar
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}-{self.celular}-{self.rut}"



# Create your models here.
class Horas(models.Model):
    hora_Horas=models.CharField(max_length=10)

    def __str__(self):
        return str(self.hora_Horas)
    

class Dias(models.Model):
    dia_Dias=models.CharField(max_length=10)
    def __str__(self):
        return str(self.dia_Dias)
    
class Tipo_servicio(models.Model):
    nombre=models.CharField(max_length=20)
    precio_servicio=models.PositiveIntegerField()
    def __str__(self):
        return str(self.nombre)
    
class Horario(models.Model):
    usuario_horario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora_horario=models.ForeignKey(Horas, on_delete=models.CASCADE)
    Tipo_servicio=models.ForeignKey(Tipo_servicio,on_delete=models.CASCADE)
    dia_horario=models.ForeignKey(Dias, on_delete=models.CASCADE)
    fecha=models.DateField(null=True,blank=True)
    ESTADOS=[
        ('P','Pendiente'),
        ('A','Atendida'),
        ('C','Cancelada')
    ]
    estado=models.CharField(max_length=1,choices=ESTADOS,default='P')
    def __str__(self):
        return str(self.usuario_horario)+"-"+str(self.hora_horario)+"-"+str(self.Tipo_servicio)+"-"+str(self.dia_horario)
    


class DiaCerrado(models.Model):
    fecha = models.DateField(unique=True)
    motivo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Día Cerrado'
        verbose_name_plural = 'Días Cerrados'

    def __str__(self):
        return f"{self.fecha} - {self.motivo or 'CERRADO'}"
