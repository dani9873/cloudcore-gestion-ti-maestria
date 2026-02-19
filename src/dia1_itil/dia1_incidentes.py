#!/usr/bin/env python3
"""
CloudCore SaaS — DÍA 1
ITIL 4: Sistema de Valor del Servicio
Gestión de Incidentes con SLA y Penalizaciones
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
import json
import os


# === CONFIGURACIÓN ===
random.seed(42)  # Para reproducibilidad
np.random.seed(42)


# Directorios de salida
BASE_DIR = os.path.expanduser('~/cloudcore_saas')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
os.makedirs(f'{OUTPUT_DIR}/reportes', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/graficos', exist_ok=True)
os.makedirs(f'{OUTPUT_DIR}/logs', exist_ok=True)


# === PARÁMETROS SLA ===
SLA_TIEMPOS = {
    'P1': 1,    # horas
    'P2': 4,
    'P3': 8,
    'P4': 24
}


PENALIZACION_HORA = {
    'P1': 5000,   # USD por hora de incumplimiento
    'P2': 2000,
    'P3': 500,
    'P4': 100
}


# === GENERACIÓN DE INCIDENTES ===
def generar_incidentes(n=15):
    """Simula incidentes del mes para CloudCore SaaS"""
    tipos = [
        'Caída base de datos',
        'Falla de autenticación',
        'Timeout en facturación',
        'Error de sincronización',
        'Sobrecarga de CPU',
        'Falla de red CDN',
        'Error en API REST',
        'Falla de backup',
        'Certificado SSL expirado',
        'Corrupción de datos'
    ]
    severidades = ['P1','P2','P3','P4']
    pesos = [0.10, 0.25, 0.35, 0.30]
    incidentes = []
    fecha_base = datetime(2024, 1, 1, 8, 0, 0)
    for i in range(n):
        sev = random.choices(severidades, weights=pesos)[0]
        sla = SLA_TIEMPOS[sev]
        # Tiempo de resolución: algunas veces excede el SLA
        if random.random() < 0.3:  # 30% incumple SLA
            tiempo_real = sla * random.uniform(1.1, 3.0)
        else:
            tiempo_real = sla * random.uniform(0.3, 0.95)
        fecha_inicio = fecha_base + timedelta(hours=random.randint(1,700))
        fecha_fin = fecha_inicio + timedelta(hours=tiempo_real)
        cumple = tiempo_real <= sla
        exceso = max(0, tiempo_real - sla)
        penalizacion = exceso * PENALIZACION_HORA[sev] if not cumple else 0
        incidentes.append({
            'id': f'INC-2024-{i+1:03d}',
            'tipo': random.choice(tipos),
            'severidad': sev,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'tiempo_real_h': round(tiempo_real, 2),
            'sla_h': sla,
            'cumple_sla': cumple,
            'exceso_h': round(exceso, 2),
            'penalizacion_usd': round(penalizacion, 2),
            'tecnico': random.choice(['Equipo Alpha','Equipo Beta','Equipo Gamma']),
            'clientes_afectados': random.randint(50, 3000) if sev == 'P1' else random.randint(1, 500)
        })
    return pd.DataFrame(incidentes)


# === ANÁLISIS SLA ===
def analizar_sla(df):
    """Calcula métricas SLA por severidad"""
    resumen = df.groupby('severidad').agg(
        total_incidentes=('id','count'),
        cumplen_sla=('cumple_sla', 'sum'),
        tiempo_promedio_h=('tiempo_real_h','mean'),
        penalizacion_total=('penalizacion_usd','sum'),
        clientes_promedio=('clientes_afectados','mean')
    ).reset_index()
    resumen['pct_cumplimiento'] = (resumen['cumplen_sla'] / resumen['total_incidentes'] * 100).round(2)
    return resumen


# === VISUALIZACIÓN ===
def generar_graficos(df, resumen):
    """Genera gráficos de análisis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('CloudCore SaaS — Dashboard ITIL 4: Gestión de Incidentes', fontsize=14, fontweight='bold')


    # Gráfico 1: Incidentes por severidad
    colores = {'P1':'#c0392b','P2':'#e67e22','P3':'#f39c12','P4':'#27ae60'}
    conteo = df['severidad'].value_counts()
    axes[0,0].bar(conteo.index, conteo.values, color=[colores.get(s,'gray') for s in conteo.index])
    axes[0,0].set_title('Incidentes por Severidad')
    axes[0,0].set_xlabel('Severidad')
    axes[0,0].set_ylabel('Cantidad')


    # Gráfico 2: Cumplimiento SLA
    labels = ['Cumple SLA', 'Incumple SLA']
    sizes = [df['cumple_sla'].sum(), (~df['cumple_sla']).sum()]
    colors_pie = ['#27ae60','#c0392b']
    axes[0,1].pie(sizes, labels=labels, colors=colors_pie, autopct='%1.1f%%', startangle=90)
    axes[0,1].set_title('Cumplimiento Global SLA')


    # Gráfico 3: Penalizaciones por severidad
    axes[1,0].bar(resumen['severidad'], resumen['penalizacion_total'],
                  color=[colores.get(s,'gray') for s in resumen['severidad']])
    axes[1,0].set_title('Penalizaciones USD por Severidad')
    axes[1,0].set_xlabel('Severidad')
    axes[1,0].set_ylabel('USD')


    # Gráfico 4: Tiempo promedio vs SLA
    x = range(len(resumen))
    width = 0.35
    axes[1,1].bar([i - width/2 for i in x], resumen['tiempo_promedio_h'], width, label='Tiempo Real', color='#3498db')
    axes[1,1].bar([i + width/2 for i in x], [SLA_TIEMPOS[s] for s in resumen['severidad']], width, label='SLA Máx', color='#e74c3c', alpha=0.6)
    axes[1,1].set_title('Tiempo Real vs SLA')
    axes[1,1].set_xticks(list(x))
    axes[1,1].set_xticklabels(resumen['severidad'])
    axes[1,1].set_ylabel('Horas')
    axes[1,1].legend()


    plt.tight_layout()
    ruta = f'{OUTPUT_DIR}/graficos/dia1_dashboard_itil.png'
    plt.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✅ Gráfico guardado: {ruta}')


# === LOG ESTRUCTURADO ===
def guardar_log(df, resumen):
    """Guarda log estructurado en JSON"""
    total_penalizacion = df['penalizacion_usd'].sum()
    tasa_cumplimiento = df['cumple_sla'].mean() * 100
    log = {
        'timestamp': datetime.now().isoformat(),
        'modulo': 'ITIL4_Gestion_Incidentes',
        'empresa': 'CloudCore SaaS',
        'total_incidentes': len(df),
        'tasa_cumplimiento_sla': round(tasa_cumplimiento, 2),
        'penalizacion_total_usd': round(total_penalizacion, 2),
        'resumen_por_severidad': resumen.to_dict('records'),
        'estado_sla': 'CUMPLE' if tasa_cumplimiento >= 95 else 'INCUMPLE'
    }
    ruta = f'{OUTPUT_DIR}/logs/dia1_itil_log.json'
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2, default=str)
    print(f'✅ Log guardado: {ruta}')
    return log


# === REPORTE CSV ===
def guardar_reporte(df):
    ruta = f'{OUTPUT_DIR}/reportes/dia1_incidentes.csv'
    df.to_csv(ruta, index=False)
    print(f'✅ Reporte CSV guardado: {ruta}')


# === MAIN ===
if __name__ == '__main__':
    print('=' * 60)
    print('CloudCore SaaS — ITIL 4 | Gestión de Incidentes')
    print('=' * 60)


    df = generar_incidentes(15)
    resumen = analizar_sla(df)


    print(f'\n📊 RESUMEN DE INCIDENTES:')
    print(df[['id','severidad','tiempo_real_h','sla_h','cumple_sla','penalizacion_usd']].to_string(index=False))
    print(f'\n📈 ANÁLISIS POR SEVERIDAD:')
    print(resumen.to_string(index=False))
    print(f'\n💰 Penalización total: USD {df["penalizacion_usd"].sum():,.2f}')
    print(f'📉 Tasa cumplimiento SLA: {df["cumple_sla"].mean()*100:.1f}%')


    generar_graficos(df, resumen)
    log = guardar_log(df, resumen)
    guardar_reporte(df)


    print('\n' + '=' * 60)
    print('✅ Día 1 completado exitosamente.')
    print('=' * 60)
