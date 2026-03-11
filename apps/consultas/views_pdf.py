# apps/consultas/views_pdf.py
# Genera receta médica en PDF usando ReportLab
import io
from datetime import date

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

from apps.core.decorators import get_rol
from .models import Consulta


# ── Paleta de colores ──────────────────────────────────────────
TEAL       = colors.HexColor('#0d9488')
TEAL_LIGHT = colors.HexColor('#f0fdfa')
TEAL_MID   = colors.HexColor('#ccfbf1')
GRAY_DARK  = colors.HexColor('#1e293b')
GRAY_MID   = colors.HexColor('#475569')
GRAY_LIGHT = colors.HexColor('#f8fafc')
GRAY_LINE  = colors.HexColor('#e2e8f0')
GREEN_BG   = colors.HexColor('#dcfce7')
GREEN_TEXT = colors.HexColor('#14532d')
WHITE      = colors.white


def _estilos():
    """Define todos los estilos de párrafo."""
    return {
        'titulo_clinica': ParagraphStyle(
            'titulo_clinica',
            fontName='Helvetica-Bold', fontSize=18,
            textColor=TEAL, leading=22, alignment=TA_LEFT,
        ),
        'subtitulo_clinica': ParagraphStyle(
            'subtitulo_clinica',
            fontName='Helvetica', fontSize=9,
            textColor=GRAY_MID, leading=12, alignment=TA_LEFT,
        ),
        'titulo_doc': ParagraphStyle(
            'titulo_doc',
            fontName='Helvetica-Bold', fontSize=13,
            textColor=WHITE, leading=18, alignment=TA_CENTER,
        ),
        'seccion': ParagraphStyle(
            'seccion',
            fontName='Helvetica-Bold', fontSize=9,
            textColor=TEAL, leading=12, spaceBefore=6,
            textTransform='uppercase',
        ),
        'etiqueta': ParagraphStyle(
            'etiqueta',
            fontName='Helvetica-Bold', fontSize=8,
            textColor=GRAY_MID, leading=11,
        ),
        'valor': ParagraphStyle(
            'valor',
            fontName='Helvetica', fontSize=9,
            textColor=GRAY_DARK, leading=12,
        ),
        'med_nombre': ParagraphStyle(
            'med_nombre',
            fontName='Helvetica-Bold', fontSize=10,
            textColor=GREEN_TEXT, leading=14,
        ),
        'med_detalle': ParagraphStyle(
            'med_detalle',
            fontName='Helvetica', fontSize=8,
            textColor=GRAY_MID, leading=11,
        ),
        'pie': ParagraphStyle(
            'pie',
            fontName='Helvetica', fontSize=7,
            textColor=GRAY_MID, leading=10, alignment=TA_CENTER,
        ),
        'firma_nombre': ParagraphStyle(
            'firma_nombre',
            fontName='Helvetica-Bold', fontSize=9,
            textColor=GRAY_DARK, leading=12, alignment=TA_CENTER,
        ),
        'firma_sub': ParagraphStyle(
            'firma_sub',
            fontName='Helvetica', fontSize=8,
            textColor=GRAY_MID, leading=11, alignment=TA_CENTER,
        ),
    }


def _fila_dato(etiqueta, valor, estilos):
    return [
        Paragraph(etiqueta, estilos['etiqueta']),
        Paragraph(str(valor) if valor else '—', estilos['valor']),
    ]


@login_required
def receta_pdf(request, pk):
    """Genera y descarga la receta médica de una consulta en PDF."""
    rol = get_rol(request.user)

    consulta = get_object_or_404(
        Consulta.objects.select_related('paciente', 'doctor').prefetch_related('recetas'),
        pk=pk
    )

    # Permiso: admin ve todo, doctor solo sus consultas
    if rol == 'DOCTOR' and consulta.doctor.usuario != request.user:
        return HttpResponseForbidden('No tienes permiso para ver esta receta.')

    # Si no tiene recetas, igual generamos la receta vacía
    recetas = list(consulta.recetas.all())

    # ── Crear el buffer PDF ──────────────────────────────────
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.5 * cm,
        bottomMargin=2 * cm,
        title=f'Receta Médica - {consulta.paciente.nombre_completo}',
        author=f'Dr. {consulta.doctor.apellidos}',
    )

    estilos = _estilos()
    story   = []
    W       = doc.width

    # ── CABECERA ─────────────────────────────────────────────
    logo_texto = Paragraph('Sullana', estilos['titulo_clinica'])
    logo_sub   = Paragraph(
        'HEALTH SYSTEM<br/>Sullana, Piura — Perú<br/>Tel: 949-021-141',
        estilos['subtitulo_clinica']
    )
    fecha_str  = consulta.fecha.strftime('%d/%m/%Y')
    num_str    = f'N.° {consulta.pk:06d}'

    cabecera = Table(
        [[logo_texto, ''],
         [logo_sub,   Paragraph(f'{fecha_str}<br/>{num_str}',
                                ParagraphStyle('r', fontName='Helvetica', fontSize=8,
                                               textColor=GRAY_MID, alignment=TA_RIGHT, leading=12))]],
        colWidths=[W * 0.65, W * 0.35],
    )
    cabecera.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN',  (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(cabecera)
    story.append(HRFlowable(width='100%', thickness=2, color=TEAL, spaceAfter=6))

    # ── BANNER "RECETA MÉDICA" ────────────────────────────────
    banner = Table(
        [[Paragraph('RECETA MÉDICA', estilos['titulo_doc'])]],
        colWidths=[W],
        rowHeights=[0.65 * cm],
    )
    banner.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, -1), TEAL),
        ('ROUNDEDCORNERS', [4]),
        ('ALIGN',       (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(banner)
    story.append(Spacer(1, 8))

    # ── DATOS DEL PACIENTE ────────────────────────────────────
    p = consulta.paciente
    edad = (date.today() - p.fecha_nacimiento).days // 365 if p.fecha_nacimiento else '—'
    dni  = p.dni or p.curp or '—'

    story.append(Paragraph('Datos del Paciente', estilos['seccion']))
    datos_paciente = Table(
        [
            _fila_dato('PACIENTE',      p.nombre_completo, estilos),
            _fila_dato('DNI',           dni,               estilos),
            _fila_dato('EDAD / SEXO',   f'{edad} años / {p.get_sexo_display()}', estilos),
            _fila_dato('FECHA CONSULTA', consulta.fecha.strftime('%d/%m/%Y %H:%M'), estilos),
        ],
        colWidths=[W * 0.25, W * 0.75],
    )
    datos_paciente.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, -1), TEAL_LIGHT),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [TEAL_LIGHT, WHITE]),
        ('TOPPADDING',  (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BOX',         (0, 0), (-1, -1), 0.5, TEAL_MID),
        ('LINEBELOW',   (0, 0), (-1, -2), 0.3, GRAY_LINE),
    ]))
    story.append(datos_paciente)
    story.append(Spacer(1, 8))

    # ── DIAGNÓSTICO ───────────────────────────────────────────
    if consulta.diagnostico:
        story.append(Paragraph('Diagnóstico', estilos['seccion']))
        diag_table = Table(
            [[Paragraph(consulta.diagnostico, estilos['valor'])]],
            colWidths=[W],
        )
        diag_table.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), GRAY_LIGHT),
            ('BOX',           (0, 0), (-1, -1), 0.5, GRAY_LINE),
            ('LEFTPADDING',   (0, 0), (-1, -1), 10),
            ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
            ('TOPPADDING',    (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(diag_table)
        story.append(Spacer(1, 8))

    # ── MEDICAMENTOS ──────────────────────────────────────────
    story.append(Paragraph(f'Medicamentos Prescritos ({len(recetas)})', estilos['seccion']))

    if recetas:
        for i, r in enumerate(recetas, start=1):
            indicaciones = r.indicaciones if r.indicaciones else ''
            bloque = Table(
                [[
                    Paragraph(f'{i}.', ParagraphStyle('n', fontName='Helvetica-Bold',
                                                       fontSize=11, textColor=TEAL)),
                    [
                        Paragraph(r.medicamento, estilos['med_nombre']),
                        Paragraph(
                            f'Dosis: <b>{r.dosis}</b> &nbsp;|&nbsp; '
                            f'Frecuencia: <b>{r.frecuencia}</b> &nbsp;|&nbsp; '
                            f'Duracion: <b>{r.duracion}</b>',
                            estilos['med_detalle']
                        ),
                    ] + ([Paragraph(f'Indicaciones: {indicaciones}', estilos['med_detalle'])]
                         if indicaciones else []),
                ]],
                colWidths=[0.7 * cm, W - 0.7 * cm],
            )
            bloque.setStyle(TableStyle([
                ('BACKGROUND',    (0, 0), (-1, -1), GREEN_BG),
                ('BOX',           (0, 0), (-1, -1), 0.5, colors.HexColor('#bbf7d0')),
                ('LEFTPADDING',   (0, 0), (-1, -1), 8),
                ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
                ('TOPPADDING',    (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(KeepTogether(bloque))
            story.append(Spacer(1, 4))
    else:
        story.append(Paragraph('Sin medicamentos prescritos en esta consulta.', estilos['valor']))

    # ── PRÓXIMA CITA ──────────────────────────────────────────
    if consulta.proxima_cita:
        story.append(Spacer(1, 6))
        prox = Table(
            [[Paragraph(
                f'Proxima cita sugerida: <b>{consulta.proxima_cita.strftime("%d/%m/%Y")}</b>',
                ParagraphStyle('pc', fontName='Helvetica', fontSize=9,
                               textColor=colors.HexColor('#92400e'))
            )]],
            colWidths=[W],
        )
        prox.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), colors.HexColor('#fef9c3')),
            ('BOX',           (0, 0), (-1, -1), 0.5, colors.HexColor('#fde047')),
            ('LEFTPADDING',   (0, 0), (-1, -1), 10),
            ('TOPPADDING',    (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(prox)

    # ── FIRMA DEL MÉDICO ─────────────────────────────────────
    story.append(Spacer(1, 20))
    d = consulta.doctor
    firma = Table(
        [[
            '',
            [
                HRFlowable(width=5 * cm, thickness=1, color=GRAY_LINE),
                Spacer(1, 3),
                Paragraph(f'Dr. {d.nombres} {d.apellidos}', estilos['firma_nombre']),
                Paragraph(d.especialidad, estilos['firma_sub']),
                Paragraph(f'Ced. Prof.: {d.cedula}', estilos['firma_sub']),
            ]
        ]],
        colWidths=[W * 0.45, W * 0.55],
    )
    firma.setStyle(TableStyle([
        ('VALIGN',  (0, 0), (-1, -1), 'BOTTOM'),
        ('ALIGN',   (1, 0), (1, -1), 'CENTER'),
    ]))
    story.append(firma)

    # ── PIE DE PÁGINA ─────────────────────────────────────────
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GRAY_LINE, spaceAfter=4))
    story.append(Paragraph(
        'Este documento es valido unicamente con firma y sello del medico tratante. '
        'Sullana Health System — Sullana, Piura, Peru.',
        estilos['pie']
    ))

    # ── Construir PDF ─────────────────────────────────────────
    doc.build(story)
    buffer.seek(0)

    nombre_archivo = (
        f"receta_{consulta.pk}_{p.apellidos.replace(' ', '_')}"
        f"_{consulta.fecha.strftime('%Y%m%d')}.pdf"
    )

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_archivo}"'
    return response
