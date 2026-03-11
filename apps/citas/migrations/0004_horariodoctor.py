# apps/citas/migrations/0004_horariodoctor.py
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        # Ajusta este nombre al último migration que tengas en citas/migrations/
        ('citas', '0003_remove_cita_citas_fecha_h_117be1_idx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HorarioDoctor',
            fields=[
                ('id',          models.AutoField(primary_key=True)),
                ('dia_semana',  models.IntegerField(
                    choices=[
                        (0,'Lunes'),(1,'Martes'),(2,'Miércoles'),
                        (3,'Jueves'),(4,'Viernes'),(5,'Sábado'),(6,'Domingo'),
                    ]
                )),
                ('hora_inicio', models.TimeField(verbose_name='Hora inicio')),
                ('hora_fin',    models.TimeField(verbose_name='Hora fin')),
                ('doctor',      models.ForeignKey(
                    to='citas.Doctor',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='horarios',
                )),
            ],
            options={
                'db_table': 'doctores_horarios',
                'ordering': ['dia_semana', 'hora_inicio'],
                'unique_together': {('doctor', 'dia_semana')},
            },
        ),
    ]