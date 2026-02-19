#!/usr/bin/env python3
"""
CloudCore SaaS — DÍA 3
COBIT 2019: Dashboard Ejecutivo y KPIs Estratégicos
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime
import json, os


np.random.seed(42)
BASE_DIR = os.path.expanduser('~/cloudcore_saas')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')


TRIMESTRES = ['Q1-2024','Q2-2024','Q3-2024','Q4-2024']


def generar_kpis():
    """Genera KPIs estratégicos trimestrales alineados con COBIT 2019"""
    datos = []
    for q in TRIMESTRES:
        disponibilidad = np.random.uniform(99.2, 99.98)
        incidentes_criticos = np.random.randint(0, 5)
        riesgo_operativo = np.random.uniform(1.5, 4.5)  # escala 1-5
        cumplimiento_sla = np.random.uniform(85, 99)
        satisfaccion_cliente = np.random.uniform(75, 95)
        tiempo_despliegue_h = np.random.uniform(1, 6)
        datos.append({
            'trimestre': q,
            'disponibilidad_pct': round(disponibilidad, 3),
            'incidentes_criticos': incidentes_criticos,
            'riesgo_operativo_score': round(riesgo_operativo, 2),
            'cumplimiento_sla_pct': round(cumplimiento_sla, 2),
            'satisfaccion_cliente_pct': round(satisfaccion_cliente, 2),
            'tiempo_despliegue_h': round(tiempo_despliegue_h, 2)
        })
    return pd.DataFrame(datos)


def calcular_nivel_madurez(df):
    """Calcula nivel de madurez COBIT (0-5)"""
    puntaje = 0
    if df['disponibilidad_pct'].mean() >= 99.9: puntaje += 1
    if df['incidentes_criticos'].mean() < 2: puntaje += 1
    if df['riesgo_operativo_score'].mean() < 3: puntaje += 1
    if df['cumplimiento_sla_pct'].mean() >= 95: puntaje += 1
    if df['satisfaccion_cliente_pct'].mean() >= 85: puntaje += 1
    niveles = {5:'Optimizado',4:'Gestionado',3:'Establecido',2:'Gestionado informalmente',1:'Inicial',0:'Inexistente'}
    return puntaje, niveles.get(puntaje, 'Inicial')


def generar_dashboard_ejecutivo(df):
    """Dashboard ejecutivo COBIT 2019"""
    fig = plt.figure(figsize=(16, 12))
    fig.patch.set_facecolor('#1a1a2e')
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)


    def style_ax(ax, title):
        ax.set_facecolor('#16213e')
        ax.set_title(title, color='white', fontsize=10, fontweight='bold', pad=8)
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('#0f3460')


    # KPI 1: Disponibilidad
    ax1 = fig.add_subplot(gs[0, 0])
    style_ax(ax1, 'Disponibilidad (%)')
    ax1.plot(TRIMESTRES, df['disponibilidad_pct'], 'o-', color='#00d4ff', linewidth=2)
    ax1.axhline(99.9, color='red', linestyle='--', alpha=0.7, label='SLA')
    ax1.set_ylim(98.5, 100.1)
    ax1.legend(facecolor='#16213e', labelcolor='white', fontsize=8)
    ax1.tick_params(axis='x', rotation=30)


    # KPI 2: Incidentes Críticos
    ax2 = fig.add_subplot(gs[0, 1])
    style_ax(ax2, 'Incidentes Críticos')
    ax2.bar(TRIMESTRES, df['incidentes_criticos'], color='#e74c3c')
    ax2.tick_params(axis='x', rotation=30)


    # KPI 3: Riesgo Operativo
    ax3 = fig.add_subplot(gs[0, 2])
    style_ax(ax3, 'Riesgo Operativo (1-5)')
    colors_risk = ['#27ae60' if v < 2.5 else '#f39c12' if v < 3.5 else '#c0392b' for v in df['riesgo_operativo_score']]
    ax3.bar(TRIMESTRES, df['riesgo_operativo_score'], color=colors_risk)
    ax3.set_ylim(0, 5)
    ax3.tick_params(axis='x', rotation=30)


    # KPI 4: Cumplimiento SLA
    ax4 = fig.add_subplot(gs[1, 0])
    style_ax(ax4, 'Cumplimiento SLA (%)')
    ax4.fill_between(range(len(TRIMESTRES)), df['cumplimiento_sla_pct'], alpha=0.6, color='#27ae60')
    ax4.plot(range(len(TRIMESTRES)), df['cumplimiento_sla_pct'], 'o-', color='#2ecc71', linewidth=2)
    ax4.set_xticks(range(len(TRIMESTRES)))
    ax4.set_xticklabels(TRIMESTRES, rotation=30, color='white')
    ax4.set_ylim(80, 102)


    # KPI 5: Satisfacción cliente
    ax5 = fig.add_subplot(gs[1, 1])
    style_ax(ax5, 'Satisfacción Cliente (%)')
    ax5.bar(TRIMESTRES, df['satisfaccion_cliente_pct'], color='#9b59b6')
    ax5.tick_params(axis='x', rotation=30)


    # Nivel de madurez
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_facecolor('#16213e')
    puntaje, nivel = calcular_nivel_madurez(df)
    ax6.text(0.5, 0.6, str(puntaje), ha='center', va='center', fontsize=60, color='#00d4ff', fontweight='bold')
    ax6.text(0.5, 0.25, nivel, ha='center', va='center', fontsize=12, color='white')
    ax6.text(0.5, 0.1, 'Nivel de Madurez COBIT', ha='center', va='center', fontsize=9, color='#aaa')
    ax6.set_xlim(0, 1); ax6.set_ylim(0, 1); ax6.axis('off')
    ax6.set_title('Madurez COBIT 2019', color='white', fontsize=10, fontweight='bold')


    # Título
    fig.text(0.5, 0.97, 'CLOUDCORE SaaS — DASHBOARD EJECUTIVO COBIT 2019', ha='center', va='top',
             fontsize=14, color='white', fontweight='bold')


    plt.tight_layout(rect=[0, 0, 1, 0.95])
    ruta = f'{OUTPUT_DIR}/graficos/dia3_dashboard_cobit.png'
    plt.savefig(ruta, dpi=150, facecolor=fig.get_facecolor(), bbox_inches='tight')
    plt.close()
    print(f'✅ Dashboard guardado: {ruta}')


if __name__ == '__main__':
    print('=' * 60)
    print('CloudCore SaaS — COBIT 2019 | Dashboard Ejecutivo')
    print('=' * 60)
    df = generar_kpis()
    print(df.to_string(index=False))
    puntaje, nivel = calcular_nivel_madurez(df)
    print(f'\n🎯 Nivel de Madurez COBIT: {puntaje}/5 — {nivel}')
    generar_dashboard_ejecutivo(df)
    df.to_csv(f'{OUTPUT_DIR}/reportes/dia3_kpis.csv', index=False)
    print('\n✅ Día 3 completado.')

