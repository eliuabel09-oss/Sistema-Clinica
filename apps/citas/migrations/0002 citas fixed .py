# Generated migration - FIXED: removed index drops that don't exist in DB
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cita',
            options={},
        ),
        migrations.AlterModelOptions(
            name='doctor',
            options={},
        ),
        # REMOVIDAS las operaciones RemoveIndex — esos índices no existen en tu BD
        # porque la tabla fue creada con SQL manual, no con Django migrations
        migrations.RemoveField(
            model_name='cita',
            name='fecha_actualizacion',
        ),
        migrations.RemoveField(
            model_name='cita',
            name='fecha_creacion',
        ),
        migrations.AddField(
            model_name='cita',
            name='informe_doctor',
            field=models.TextField(blank=True, help_text='El doctor puede dejar indicaciones previas o posteriores a la consulta', verbose_name='Informe del doctor'),
        ),
        migrations.AddField(
            model_name='cita',
            name='informe_fecha',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha del informe'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='biografia',
            field=models.TextField(blank=True, verbose_name='Biografía / Presentación'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='doctores/'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='horario_atencion',
            field=models.CharField(blank=True, max_length=200, verbose_name='Horario de atención'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='usuario',
            field=models.OneToOneField(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='doctor_perfil',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Usuario del sistema'
            ),
        ),
        migrations.AlterField(
            model_name='cita',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='citas.doctor'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='duracion_min',
            field=models.PositiveIntegerField(default=30, verbose_name='Duración (min)'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='estado',
            field=models.CharField(
                choices=[
                    ('PENDIENTE',  'Pendiente'),
                    ('CONFIRMADA', 'Confirmada'),
                    ('CANCELADA',  'Cancelada'),
                    ('COMPLETADA', 'Completada'),
                    ('NO_ASISTIO', 'No asistió'),
                ],
                default='PENDIENTE', max_length=20
            ),
        ),
        migrations.AlterField(
            model_name='cita',
            name='fecha_hora',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='cita',
            name='motivo',
            field=models.TextField(blank=True, verbose_name='Motivo de consulta'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='notas_admin',
            field=models.TextField(blank=True, verbose_name='Notas administrativas'),
        ),
        migrations.AlterField(
            model_name='cita',
            name='paciente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='citas', to='pacientes.paciente'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='telefono',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]