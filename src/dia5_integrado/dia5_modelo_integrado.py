#!/usr/bin/env python3
"""
CloudCore SaaS — DÍA 5
MODELO INTEGRADO: ITIL 4 + ISO 20000 + COBIT 2019 + ISO 22301
Dashboard ejecutivo + Informe PDF automático
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import cm
from datetime import datetime
import json, os, sys


np.random.seed(42)
BASE_DIR = os.path.expanduser('~/cloudcore_saas')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(f'{OUTPUT_DIR}/pdf', exist_ok=True)


# =============================================
# MÓDULO 1: GESTIÓN DE INCIDENTES (ITIL 4)
# =============================================
def modulo_incidentes():
    SLA = {'P1':1,'P2':4,'P3':8,'P4':24}
    severidades = np.random.choice(['P1','P2','P3','P4'], 20, p=[0.1,0.2,0.4,0.3])
    resultados = []
    for sev in severidades:
        t = SLA[sev] * np.random.uniform(0.4, 2.0)
        resultados.append({'severidad':sev, 'tiempo_h':round(t,2), 'cumple':t<=SLA[sev]})
    df = pd.DataFrame(resultados)
    tasa = df['cumple'].mean() * 100
    return df, round(tasa, 2)


# =============================================
# MÓDULO 2: DISPONIBILIDAD (ISO 20000)
# =============================================
def modulo_disponibilidad():
    meses = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    uptimes = np.random.uniform(99.0, 99.99, 12)
    uptimes[2] = 98.8; uptimes[7] = 99.1  # simulamos meses problemáticos
    df = pd.DataFrame({'mes':meses,'uptime':uptimes.round(3)})
    uptime_anual = uptimes.mean()
    return df, round(uptime_anual, 3)


# =============================================
# MÓDULO 3: KPIs COBIT
# =============================================
def modulo_kpis():
    kpis = {
        'Disponibilidad': 99.72,
        'Cumplimiento SLA': 87.5,
        'Satisfacción Cliente': 82.3,
        'Riesgo Operativo (inv)': 68.0,  # invertido: mayor es mejor
        'Tiempo Despliegue (inv)': 75.0
    }
    return kpis


# =============================================
# MÓDULO 4: CONTINUIDAD (ISO 22301)
# =============================================
def modulo_continuidad():
    escenarios = [
        {'nombre':'BD Fallo','rto_real':np.random.uniform(2,7),'rto_obj':4.0},
        {'nombre':'Ransomware','rto_real':np.random.uniform(8,24),'rto_obj':4.0},
        {'nombre':'Cloud Down','rto_real':np.random.uniform(1,5),'rto_obj':4.0},
    ]
    for e in escenarios:
        e['cumple'] = e['rto_real'] <= e['rto_obj']
        e['impacto_usd'] = e['rto_real'] * 15000
    df = pd.DataFrame(escenarios)
    return df


# =============================================
# NIVEL DE MADUREZ INTEGRADO
# =============================================
def calcular_madurez(tasa_sla, uptime, kpis, df_cont):
    puntaje = 0
    if tasa_sla >= 90: puntaje += 1
    if uptime >= 99.9: puntaje += 1
    if kpis['Cumplimiento SLA'] >= 90: puntaje += 1
    if df_cont['cumple'].mean() >= 0.6: puntaje += 1
    if kpis['Satisfacción Cliente'] >= 80: puntaje += 1
    niveles = {5:'Optimizado (Nivel 5)',4:'Gestionado (Nivel 4)',
               3:'Establecido (Nivel 3)',2:'Gestionado Informalmente (Nivel 2)',
               1:'Inicial (Nivel 1)',0:'Inexistente (Nivel 0)'}
    return puntaje, niveles.get(puntaje,'Inicial')


# =============================================
# DASHBOARD INTEGRADO
# =============================================
def dashboard_integrado(df_inc, df_disp, kpis, df_cont, tasa_sla, uptime, madurez_txt):
    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor('#0d1117')
    gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.45, wspace=0.3)


    def style(ax, title):
        ax.set_facecolor('#161b22')
        ax.set_title(title, color='#f0f6fc', fontsize=9, fontweight='bold', pad=6)
        ax.tick_params(colors='#8b949e', labelsize=8)
        for spine in ax.spines.values(): spine.set_color('#30363d')


    # Incidentes
    ax1 = fig.add_subplot(gs[0,0])
    style(ax1, 'Incidentes por Severidad')
    cnt = df_inc['severidad'].value_counts().sort_index()
    colors_bar = ['#f85149','#f0883e','#d29922','#3fb950']
    ax1.bar(cnt.index, cnt.values, color=colors_bar[:len(cnt)])


    # Cumplimiento SLA
    ax2 = fig.add_subplot(gs[0,1])
    style(ax2, f'SLA {tasa_sla:.1f}%')
    cumple = df_inc['cumple'].sum(); incumple = len(df_inc) - cumple
    ax2.pie([cumple, incumple], labels=['Cumple','Incumple'],
            colors=['#3fb950','#f85149'], autopct='%1.0f%%', textprops={'color':'white','fontsize':8})


    # Disponibilidad mensual
    ax3 = fig.add_subplot(gs[0,2:4])
    style(ax3, f'Disponibilidad Mensual (Anual: {uptime:.3f}%)')
    c_up = ['#3fb950' if u >= 99.9 else '#f85149' for u in df_disp['uptime']]
    ax3.bar(df_disp['mes'], df_disp['uptime'], color=c_up)
    ax3.axhline(99.9, color='#58a6ff', linestyle='--', linewidth=1.5, label='SLA 99.9%')
    ax3.set_ylim(98, 100.05)
    ax3.legend(facecolor='#161b22', labelcolor='white', fontsize=8)
    ax3.tick_params(axis='x', rotation=45)


    # KPIs Radar
    ax4 = fig.add_subplot(gs[1,0:2], polar=True)
    ax4.set_facecolor('#161b22')
    labels_kpi = list(kpis.keys())
    valores = list(kpis.values())
    N = len(labels_kpi)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    valores_plot = valores + valores[:1]
    ax4.plot(angles, valores_plot, 'o-', color='#58a6ff', linewidth=2)
    ax4.fill(angles, valores_plot, alpha=0.25, color='#58a6ff')
    ax4.set_xticks(angles[:-1])
    ax4.set_xticklabels(labels_kpi, color='white', size=7)
    ax4.set_ylim(0, 100)
    ax4.set_title('KPIs COBIT 2019', color='white', size=9, fontweight='bold', pad=15)
    ax4.tick_params(colors='#8b949e')
    ax4.spines['polar'].set_color('#30363d')


    # Continuidad RTO
    ax5 = fig.add_subplot(gs[1,2:4])
    style(ax5, 'Continuidad: RTO Real vs Objetivo')
    c_rto = ['#3fb950' if c else '#f85149' for c in df_cont['cumple']]
    ax5.barh(df_cont['nombre'], df_cont['rto_real'], color=c_rto)
    ax5.axvline(4.0, color='#58a6ff', linestyle='--', linewidth=2, label='RTO Obj 4h')
    ax5.legend(facecolor='#161b22', labelcolor='white', fontsize=8)


    # Nivel madurez
    ax6 = fig.add_subplot(gs[2,1:3])
    ax6.set_facecolor('#161b22')
    ax6.axis('off')
    madurez_num = madurez_txt.split('(')[1].split(')')[0].split(' ')[-1] if '(' in madurez_txt else '?'
    ax6.text(0.5, 0.65, madurez_num, ha='center', va='center', fontsize=80,
             color='#58a6ff', fontweight='bold', transform=ax6.transAxes)
    ax6.text(0.5, 0.3, madurez_txt, ha='center', va='center', fontsize=12,
             color='white', transform=ax6.transAxes)
    ax6.set_title('Nivel de Madurez Integrado', color='white', size=10, fontweight='bold')


    fig.text(0.5, 0.985, '🚀 CLOUDCORE SaaS — MODELO INTEGRADO ITIL4+ISO20000+COBIT2019+ISO22301',
             ha='center', va='top', fontsize=13, color='white', fontweight='bold')
    fig.text(0.5, 0.965, f'Generado: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', va='top', fontsize=9, color='#8b949e')


    plt.tight_layout(rect=[0,0,1,0.95])
    ruta = f'{OUTPUT_DIR}/graficos/dia5_dashboard_integrado.png'
    plt.savefig(ruta, dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f'✅ Dashboard integrado: {ruta}')


# =============================================
# GENERACIÓN PDF CON REPORTLAB
# =============================================
def generar_pdf(tasa_sla, uptime, kpis, df_cont, puntaje_madurez, madurez_txt):
    ruta_pdf = f'{OUTPUT_DIR}/pdf/informe_final_cloudcore.pdf'
    doc = SimpleDocTemplate(ruta_pdf, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []


    titulo_style = ParagraphStyle('Titulo', parent=styles['Title'],
                                   fontSize=20, textColor=colors.HexColor('#1F4E79'),
                                   spaceAfter=6)
    h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
                               fontSize=14, textColor=colors.HexColor('#2E75B6'),
                               spaceAfter=6, spaceBefore=16)
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
                               fontSize=12, textColor=colors.HexColor('#1F4E79'),
                               spaceAfter=4, spaceBefore=10)
    normal = styles['Normal']
    normal.fontSize = 10
    normal.leading = 14


    # Portada
    story.append(Paragraph('INFORME EJECUTIVO FINAL', titulo_style))
    story.append(Paragraph('CloudCore SaaS — Sistema Integrado de Gestión TI', styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width='100%', thickness=2, color=colors.HexColor('#2E75B6')))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f'Fecha de generación: {datetime.now().strftime("%d/%m/%Y %H:%M")}', normal))
    story.append(Paragraph('Marcos aplicados: ITIL 4 | ISO/IEC 20000 | COBIT 2019 | ISO 22301', normal))
    story.append(Spacer(1, 0.5*cm))


    # Resumen ejecutivo
    story.append(Paragraph('1. RESUMEN EJECUTIVO', h1_style))
    resumen = f'''CloudCore SaaS opera una plataforma crítica de facturación electrónica para 3,000 empresas 
    con dependencia 100% en TI. Este informe consolida los resultados del análisis integrado bajo cuatro marcos 
    de referencia internacionales. El nivel de madurez alcanzado es <b>{madurez_txt}</b>, con una tasa de 
    cumplimiento SLA de incidentes de <b>{tasa_sla}%</b> y disponibilidad anual promedio de <b>{uptime}%</b>.'''
    story.append(Paragraph(resumen, normal))
    story.append(Spacer(1, 0.3*cm))


    # Tabla de indicadores clave
    story.append(Paragraph('2. INDICADORES CLAVE DE DESEMPEÑO', h1_style))
    tabla_data = [['Indicador','Valor','Marco','Estado']]
    tabla_data.append(['Disponibilidad Anual', f'{uptime}%', 'ISO 20000', '✓ CUMPLE' if uptime >= 99.9 else '✗ ALERTA'])
    tabla_data.append(['Cumplimiento SLA Incidentes', f'{tasa_sla}%', 'ITIL 4', '✓ OK' if tasa_sla >= 90 else '✗ REVISAR'])
    for k, v in kpis.items():
        tabla_data.append([k, f'{v}%', 'COBIT 2019', '✓ OK' if v >= 80 else '⚠ REVISAR'])
    tabla_data.append(['RTO Cumplimiento', f"{df_cont['cumple'].mean()*100:.0f}%", 'ISO 22301', '✓ OK' if df_cont['cumple'].mean() >= 0.6 else '✗ CRÍTICO'])


    t = Table(tabla_data, colWidths=[6*cm, 3*cm, 3.5*cm, 2.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F4E79')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#EBF5FB'), colors.white]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.5*cm))


    # Análisis por marco
    story.append(Paragraph('3. ANÁLISIS POR MARCO DE REFERENCIA', h1_style))


    story.append(Paragraph('3.1 ITIL 4 — Gestión de Incidentes', h2_style))
    story.append(Paragraph(f'La tasa de cumplimiento SLA alcanzó el {tasa_sla}%. Los incidentes P1 representan el mayor riesgo operativo con impacto en todos los clientes simultáneamente. Se recomienda automatizar la detección y escalamiento.', normal))


    story.append(Paragraph('3.2 ISO/IEC 20000 — Disponibilidad', h2_style))
    estado_disp = 'cumple' if uptime >= 99.9 else 'no cumple'
    story.append(Paragraph(f'La disponibilidad anual promedio de {uptime}% {estado_disp} el SLA objetivo de 99.9%. Tres meses presentaron caídas por debajo del umbral aceptable, requiriendo plan de mejora inmediato.', normal))


    story.append(Paragraph('3.3 COBIT 2019 — Gobernanza', h2_style))
    story.append(Paragraph('El comité de gobierno TI identificó brechas en satisfacción del cliente y cumplimiento SLA que requieren inversión en capacidad y automatización de procesos de recuperación.', normal))


    story.append(Paragraph('3.4 ISO 22301 — Continuidad', h2_style))
    esc_criticos = df_cont[~df_cont['cumple']]['nombre'].tolist()
    story.append(Paragraph(f'Los escenarios que incumplen el RTO objetivo de 4 horas son: {esc_criticos}. El impacto financiero potencial acumulado supera los USD {df_cont["impacto_usd"].sum():,.0f}. Se requiere actualización urgente del DRP.', normal))
    story.append(Spacer(1, 0.3*cm))


    # Nivel de madurez
    story.append(Paragraph('4. EVALUACIÓN DE MADUREZ', h1_style))
    story.append(Paragraph(f'El nivel de madurez integrado evaluado según COBIT 2019 es: <b>{madurez_txt}</b> ({puntaje_madurez}/5 criterios cumplidos).', normal))


    madurez_tabla = [['Criterio','Estado','Puntaje'],
        [f'Disponibilidad ≥ 99.9%', '✓' if uptime >= 99.9 else '✗', '1' if uptime >= 99.9 else '0'],
        [f'SLA Incidentes ≥ 90%', '✓' if tasa_sla >= 90 else '✗', '1' if tasa_sla >= 90 else '0'],
        ['Cumplimiento SLA COBIT ≥ 90%', '✓' if kpis['Cumplimiento SLA'] >= 90 else '✗', '1' if kpis['Cumplimiento SLA'] >= 90 else '0'],
        ['RTO Cumplimiento ≥ 60%', '✓' if df_cont['cumple'].mean() >= 0.6 else '✗', '1' if df_cont['cumple'].mean() >= 0.6 else '0'],
        ['Satisfacción Cliente ≥ 80%', '✓' if kpis['Satisfacción Cliente'] >= 80 else '✗', '1' if kpis['Satisfacción Cliente'] >= 80 else '0'],
    ]
    tm = Table(madurez_tabla, colWidths=[9*cm, 2*cm, 2*cm])
    tm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E75B6')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BDC3C7')),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(tm)
    story.append(Spacer(1, 0.5*cm))


    # Recomendaciones
    story.append(Paragraph('5. RECOMENDACIONES ESTRATÉGICAS', h1_style))
    recomendaciones = [
        '1. Implementar monitoreo proactivo 24/7 con alertas automatizadas para incidentes P1/P2.',
        '2. Establecer réplica geográfica activo-activo para eliminar single points of failure en BD.',
        '3. Actualizar el DRP con procedimientos específicos para ransomware con tiempo objetivo < 4h.',
        '4. Crear un comité de Continuidad de Negocio con reuniones quincenales y KPIs formales.',
        '5. Implementar chaos engineering para validar RTO en entornos de staging mensualmente.',
        '6. Certificar el SMS bajo ISO/IEC 20000 para fortalecer la confianza de los clientes.',
        '7. Aumentar la inversión en capacitación del equipo ITSM para reducir tiempo de resolución.',
    ]
    for r in recomendaciones:
        story.append(Paragraph(r, normal))
        story.append(Spacer(1, 0.15*cm))


    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#BDC3C7')))
    story.append(Paragraph('Documento generado automáticamente por CloudCore SaaS — Sistema Integrado de Gestión TI', 
                            ParagraphStyle('footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))


    doc.build(story)
    print(f'✅ PDF generado: {ruta_pdf}')
    return ruta_pdf


# =============================================
# MAIN
# =============================================
if __name__ == '__main__':
    print('=' * 60)
    print('CloudCore SaaS — MODELO INTEGRADO FINAL')
    print('=' * 60)


    df_inc, tasa_sla = modulo_incidentes()
    df_disp, uptime = modulo_disponibilidad()
    kpis = modulo_kpis()
    df_cont = modulo_continuidad()
    puntaje, madurez_txt = calcular_madurez(tasa_sla, uptime, kpis, df_cont)


    print(f'\n📊 Tasa SLA Incidentes: {tasa_sla}%')
    print(f'📈 Uptime anual: {uptime}%')
    print(f'🎯 Madurez: {madurez_txt} ({puntaje}/5)')
    print(f'\nEscenarios Continuidad:')
    print(df_cont[['nombre','rto_real','cumple','impacto_usd']].to_string(index=False))


    dashboard_integrado(df_inc, df_disp, kpis, df_cont, tasa_sla, uptime, madurez_txt)
    pdf = generar_pdf(tasa_sla, uptime, kpis, df_cont, puntaje, madurez_txt)


    print('\n' + '=' * 60)
    print('✅ MODELO INTEGRADO COMPLETADO')
    print(f'📄 PDF: {pdf}')
    print('=' * 60)

