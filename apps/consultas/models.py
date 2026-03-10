# apps/consultas/models.py
from django.db import models
from apps.pacientes.models import Paciente
from apps.citas.models import Cita, Doctor


class Consulta(models.Model):
    cita        = models.OneToOneField(
        Cita, on_delete=models.PROTECT,
        related_name='consulta', null=True, blank=True
    )
    paciente    = models.ForeignKey(
        Paciente, on_delete=models.PROTECT,
        related_name='consultas', db_index=True
    )
    doctor      = models.ForeignKey(
        Doctor, on_delete=models.PROTECT,
        related_name='consultas'
    )
    fecha       = models.DateTimeField(auto_now_add=True, db_index=True)

    # Signos vitales
    peso_kg         = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    talla_cm        = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    presion_arterial= models.CharField(max_length=10, blank=True, help_text="Ej: 120/80")
    frecuencia_cardiaca = models.PositiveSmallIntegerField(null=True, blank=True, help_text="lpm")
    temperatura     = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°C")
    saturacion_o2   = models.PositiveSmallIntegerField(null=True, blank=True, help_text="%")

    # Nota médica SOAP
    subjetivo       = models.TextField(help_text="Motivo de consulta y síntomas referidos")
    objetivo        = models.TextField(help_text="Exploración física y hallazgos")
    diagnostico     = models.TextField(help_text="Diagnóstico (puede incluir CIE-10)")
    plan            = models.TextField(help_text="Plan de tratamiento y recomendaciones")
    evolucion       = models.TextField(blank=True, help_text="Notas de evolución adicionales")

    proxima_cita    = models.DateField(null=True, blank=True, help_text="Fecha sugerida para próxima cita")

    class Meta:
        db_table    = 'consultas'
        ordering    = ['-fecha']
        indexes     = [
            models.Index(fields=['paciente', 'fecha']),
        ]
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

    def __str__(self):
        return f"Consulta {self.pk} — {self.paciente} ({self.fecha:%d/%m/%Y})"

    @property
    def imc(self):
        if self.peso_kg and self.talla_cm and self.talla_cm > 0:
            talla_m = float(self.talla_cm) / 100
            return round(float(self.peso_kg) / (talla_m ** 2), 2)
        return None


class Receta(models.Model):
    consulta    = models.ForeignKey(
        Consulta, on_delete=models.CASCADE,
        related_name='recetas'
    )
    medicamento = models.CharField(max_length=200)
    dosis       = models.CharField(max_length=100, help_text="Ej: 500 mg")
    frecuencia  = models.CharField(max_length=100, help_text="Ej: Cada 8 horas")
    duracion    = models.CharField(max_length=100, help_text="Ej: 7 días")
    indicaciones= models.TextField(blank=True, help_text="Instrucciones especiales")
    orden       = models.PositiveSmallIntegerField(default=1)

    class Meta:
        db_table    = 'recetas'
        ordering    = ['consulta', 'orden']
        verbose_name = 'Receta'
        verbose_name_plural = 'Recetas'

    def __str__(self):
        return f"{self.medicamento} {self.dosis} — {self.frecuencia}"
