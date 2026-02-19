#!/usr/bin/env python3
"""
CloudCore SaaS — DÍA 2
ISO/IEC 20000: Gestión de Disponibilidad
Cálculo de uptime mensual y evaluación SLA
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import json, os


random_seed = 42
np.random.seed(random_seed)


BASE_DIR = os.path.expanduser('~/cloudcore_saas')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')


SLA_DISPONIBILIDAD = 99.9  # %
HORAS_MES = 730  # horas promedio por mes
COSTO_DOWNTIME_HORA = 15000  # USD


MESES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']


def simular_disponibilidad():
    """Simula disponibilidad mensual durante 12 meses"""
    datos = []
    for i, mes in enumerate(MESES):
        # La mayoría de meses cumple SLA, algunos no
        if i in [2, 7, 10]:  # Meses con incidentes mayores
            uptime_pct = np.random.uniform(98.5, 99.7)
        else:
            uptime_pct = np.random.uniform(99.85, 99.99)
        horas_down = HORAS_MES * (1 - uptime_pct / 100)
        cumple = uptime_pct >= SLA_DISPONIBILIDAD
        impacto = horas_down * COSTO_DOWNTIME_HORA
        datos.append({
            'mes': mes,
            'uptime_pct': round(uptime_pct, 4),
            'horas_down': round(horas_down, 2),
            'minutos_down': round(horas_down * 60, 1),
            'cumple_sla': cumple,
            'impacto_financiero_usd': round(impacto, 2)
        })
    return pd.DataFrame(datos)


def generar_reporte_tecnico(df):
    """Genera reporte técnico de disponibilidad"""
    uptime_anual = df['uptime_pct'].mean()
    meses_incumplidos = df[~df['cumple_sla']]['mes'].tolist()
    impacto_total = df['impacto_financiero_usd'].sum()
    reporte = {
        'fecha_generacion': datetime.now().isoformat(),
        'norma': 'ISO/IEC 20000',
        'empresa': 'CloudCore SaaS',
        'sla_objetivo': f'{SLA_DISPONIBILIDAD}%',
        'uptime_anual_promedio': f'{uptime_anual:.4f}%',
        'meses_que_cumplen_sla': df['cumple_sla'].sum(),
        'meses_que_incumplen': len(meses_incumplidos),
        'meses_incumplidos': meses_incumplidos,
        'impacto_financiero_total_usd': round(impacto_total, 2),
        'estado_global': 'CUMPLE' if uptime_anual >= SLA_DISPONIBILIDAD else 'REQUIERE_MEJORA'
    }
    ruta = f'{OUTPUT_DIR}/reportes/dia2_disponibilidad_reporte.json'
    with open(ruta, 'w') as f:
        json.dump(reporte, f, indent=2, default=lambda x: int(x) if hasattr(x, "__int__") else str(x))
    print(f'✅ Reporte técnico: {ruta}')
    return reporte


def generar_graficos(df):
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('CloudCore SaaS — ISO/IEC 20000: Disponibilidad Anual', fontsize=13, fontweight='bold')


    colores = ['#27ae60' if c else '#c0392b' for c in df['cumple_sla']]
    axes[0].bar(df['mes'], df['uptime_pct'], color=colores)
    axes[0].axhline(y=SLA_DISPONIBILIDAD, color='navy', linestyle='--', linewidth=2, label=f'SLA {SLA_DISPONIBILIDAD}%')
    axes[0].set_ylim(98, 100.05)
    axes[0].set_title('Disponibilidad Mensual (%)')
    axes[0].set_ylabel('Uptime %')
    axes[0].legend()
    axes[0].tick_params(axis='x', rotation=45)


    verde = mpatches.Patch(color='#27ae60', label='Cumple SLA')
    rojo = mpatches.Patch(color='#c0392b', label='Incumple SLA')
    axes[0].legend(handles=[verde, rojo, plt.Line2D([0],[0], color='navy', linestyle='--', label=f'SLA {SLA_DISPONIBILIDAD}%')])


    axes[1].bar(df['mes'], df['impacto_financiero_usd'], color='#e74c3c', alpha=0.8)
    axes[1].set_title('Impacto Financiero por Downtime (USD)')
    axes[1].set_ylabel('USD')
    axes[1].tick_params(axis='x', rotation=45)


    plt.tight_layout()
    ruta = f'{OUTPUT_DIR}/graficos/dia2_disponibilidad.png'
    plt.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✅ Gráfico guardado: {ruta}')


if __name__ == '__main__':
    print('=' * 60)
    print('CloudCore SaaS — ISO/IEC 20000 | Disponibilidad')
    print('=' * 60)
    df = simular_disponibilidad()
    print(df.to_string(index=False))
    reporte = generar_reporte_tecnico(df)
    generar_graficos(df)
    df.to_csv(f'{OUTPUT_DIR}/reportes/dia2_disponibilidad.csv', index=False)
    print(f'\n📊 Uptime anual promedio: {df["uptime_pct"].mean():.4f}%')
    print(f'💰 Impacto financiero total: USD {df["impacto_financiero_usd"].sum():,.2f}')
    print('\n✅ Día 2 completado.')

