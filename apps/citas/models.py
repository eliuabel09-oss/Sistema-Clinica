# apps/citas/models.py — VERSIÓN ACTUALIZADA
# Reemplaza SOLO el modelo Doctor (el modelo Cita se muestra completo abajo)
from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    # Campos originales (no tocar)
    nombres      = models.CharField(max_length=100)
    apellidos    = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    cedula       = models.CharField(max_length=20, unique=True)
    telefono     = models.CharField(max_length=20, blank=True)
    email        = models.EmailField(blank=True)
    activo       = models.BooleanField(default=True)

    # NUEVOS campos
    usuario      = models.OneToOneField(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='doctor_perfil',
        verbose_name='Usuario del sistema'
    )
    foto            = models.ImageField(upload_to='doctores/', null=True, blank=True)
    biografia       = models.TextField(blank=True, verbose_name='Biografía / Presentación')
    horario_atencion= models.CharField(max_length=200, blank=True, verbose_name='Horario de atención')

    class Meta:
        db_table = 'doctores'

    def __str__(self):
        return f'Dr. {self.apellidos}, {self.nombres}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'


class Cita(models.Model):
    TIPO_CHOICES = [
        ('PRIMERA_VEZ',  'Primera vez'),
        ('SEGUIMIENTO',  'Seguimiento'),
        ('URGENCIA',     'Urgencia'),
        ('REVISION',     'Revisión de resultados'),
    ]
    ESTADO_CHOICES = [
        ('PENDIENTE',   'Pendiente'),
        ('CONFIRMADA',  'Confirmada'),
        ('CANCELADA',   'Cancelada'),
        ('COMPLETADA',  'Completada'),
        ('NO_ASISTIO',  'No asistió'),
    ]

    paciente     = models.ForeignKey('pacientes.Paciente', on_delete=models.CASCADE, related_name='citas')
    doctor       = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='citas')
    fecha_hora   = models.DateTimeField()
    duracion_min = models.PositiveIntegerField(default=30, verbose_name='Duración (min)')
    tipo         = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PRIMERA_VEZ')
    estado       = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    motivo       = models.TextField(blank=True, verbose_name='Motivo de consulta')
    notas_admin  = models.TextField(blank=True, verbose_name='Notas administrativas')

    # NUEVOS campos
    informe_doctor = models.TextField(
        blank=True,
        verbose_name='Informe del doctor',
        help_text='El doctor puede dejar indicaciones previas o posteriores a la consulta'
    )
    informe_fecha  = models.DateTimeField(null=True, blank=True, verbose_name='Fecha del informe')

    class Meta:
        db_table = 'citas'

    def __str__(self):
        return f'{self.paciente} — {self.doctor} — {self.fecha_hora:%d/%m/%Y %H:%M}'