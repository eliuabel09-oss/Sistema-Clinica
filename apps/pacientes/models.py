# apps/pacientes/models.py
from django.db import models
from django.utils import timezone


class Paciente(models.Model):
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    TIPO_SANGRE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    # Datos personales
    nombres          = models.CharField(max_length=100, db_index=True)
    apellidos        = models.CharField(max_length=100, db_index=True)
    fecha_nacimiento = models.DateField()
    sexo             = models.CharField(max_length=1, choices=SEXO_CHOICES)

    # FIX: campo dni agregado (Perú usa DNI, no CURP que es mexicano)
    # curp se mantiene para no romper la BD existente
    dni              = models.CharField(
        max_length=8, blank=True, null=True,
        verbose_name='DNI',
        help_text='Documento Nacional de Identidad (8 dígitos)'
    )
    curp             = models.CharField(max_length=18, unique=True, blank=True, null=True)
    tipo_sangre      = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES, blank=True)

    # Contacto
    telefono         = models.CharField(max_length=15)
    email            = models.EmailField(blank=True, null=True)
    direccion        = models.TextField(blank=True)

    # Datos médicos generales
    alergias              = models.TextField(blank=True, help_text='Lista de alergias conocidas')
    antecedentes          = models.TextField(blank=True, help_text='Antecedentes heredofamiliares')
    enfermedades_cronicas = models.TextField(blank=True)

    # Metadatos
    activo              = models.BooleanField(default=True)
    fecha_registro      = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pacientes'
        ordering = ['apellidos', 'nombres']
        indexes  = [
            models.Index(fields=['apellidos', 'nombres']),
            models.Index(fields=['curp']),
        ]
        verbose_name        = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.apellidos}, {self.nombres}'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'

    @property
    def edad(self):
        hoy   = timezone.now().date()
        delta = hoy - self.fecha_nacimiento
        return delta.days // 365

    @property
    def documento(self):
        """Devuelve DNI si existe, si no CURP, si no vacío."""
        return self.dni or self.curp or '—'


class ArchivoClinico(models.Model):
    TIPO_CHOICES = [
        ('PDF',  'Documento PDF'),
        ('IMG',  'Imagen'),
        ('LAB',  'Resultado de Laboratorio'),
        ('RX',   'Radiografía'),
        ('OTRO', 'Otro'),
    ]

    paciente    = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='archivos')
    tipo        = models.CharField(max_length=10, choices=TIPO_CHOICES)
    nombre      = models.CharField(max_length=200)
    archivo     = models.FileField(upload_to='archivos_clinicos/%Y/%m/')
    descripcion = models.TextField(blank=True)
    fecha_carga = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table            = 'archivos_clinicos'
        ordering            = ['-fecha_carga']
        verbose_name        = 'Archivo Clínico'
        verbose_name_plural = 'Archivos Clínicos'

    def __str__(self):
        return f'{self.nombre} — {self.paciente}'