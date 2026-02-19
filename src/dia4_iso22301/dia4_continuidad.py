#!/usr/bin/env python3
"""
CloudCore SaaS — DÍA 4
ISO 22301: Continuidad del Negocio
Simulación de escenarios de crisis y cálculo RTO
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json, os


np.random.seed(42)
BASE_DIR = os.path.expanduser('~/cloudcore_saas')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')


RTO_OBJETIVO = 4.0  # horas
RPO_OBJETIVO = 0.25  # horas (15 min)
COSTO_HORA = 15000  # USD
CLIENTES = 3000


ESCENARIOS = [
    {
        'id': 'ESC-001',
        'nombre': 'Fallo Total de Base de Datos',
        'tipo': 'Infraestructura',
        'probabilidad': 0.15,
        'rto_real_h': np.random.uniform(2.5, 6.5),
        'rpo_real_h': np.random.uniform(0.1, 0.5),
        'clientes_impactados': 3000,
        'descripcion': 'Corrupción crítica de datos en PostgreSQL principal. Replica no sincronizada.'
    },
    {
        'id': 'ESC-002',
        'nombre': 'Ataque Ransomware',
        'tipo': 'Ciberseguridad',
        'probabilidad': 0.08,
        'rto_real_h': np.random.uniform(8.0, 24.0),
        'rpo_real_h': np.random.uniform(1.0, 4.0),
        'clientes_impactados': 3000,
        'descripcion': 'Cifrado de archivos críticos. Servidores de aplicación comprometidos.'
    },
    {
        'id': 'ESC-003',
        'nombre': 'Caída de Infraestructura Cloud',
        'tipo': 'Proveedor Cloud',
        'probabilidad': 0.12,
        'rto_real_h': np.random.uniform(1.5, 5.0),
        'rpo_real_h': np.random.uniform(0.05, 0.3),
        'clientes_impactados': np.random.randint(1500, 3000),
        'descripcion': 'Falla en zona de disponibilidad AWS us-east-1. Failover no activado.'
    },
    {
        'id': 'ESC-004',
        'nombre': 'Pérdida de Conectividad de Red',
        'tipo': 'Redes',
        'probabilidad': 0.20,
        'rto_real_h': np.random.uniform(0.5, 3.0),
        'rpo_real_h': 0.0,
        'clientes_impactados': np.random.randint(500, 2000),
        'descripcion': 'Falla ISP primario. Failover a ISP secundario tardó más de lo esperado.'
    },
    {
        'id': 'ESC-005',
        'nombre': 'Error Crítico en Despliegue',
        'tipo': 'Operaciones',
        'probabilidad': 0.25,
        'rto_real_h': np.random.uniform(0.5, 2.5),
        'rpo_real_h': 0.0,
        'clientes_impactados': np.random.randint(100, 800),
        'descripcion': 'Rollback necesario tras deploy fallido. Scripts de migración con errores.'
    },
]


def analizar_escenarios():
    resultados = []
    for esc in ESCENARIOS:
        rto_real = esc['rto_real_h']
        rpo_real = esc['rpo_real_h']
        cumple_rto = rto_real <= RTO_OBJETIVO
        cumple_rpo = rpo_real <= RPO_OBJETIVO
        costo = rto_real * COSTO_HORA
        riesgo_residual = esc['probabilidad'] * costo
        resultados.append({
            'id': esc['id'],
            'escenario': esc['nombre'],
            'tipo': esc['tipo'],
            'probabilidad': esc['probabilidad'],
            'rto_real_h': round(rto_real, 2),
            'rto_objetivo_h': RTO_OBJETIVO,
            'cumple_rto': cumple_rto,
            'rpo_real_h': round(rpo_real, 2),
            'rpo_objetivo_h': RPO_OBJETIVO,
            'cumple_rpo': cumple_rpo,
            'clientes_impactados': int(esc['clientes_impactados']),
            'impacto_financiero_usd': round(costo, 2),
            'riesgo_residual_usd': round(riesgo_residual, 2),
        })
    return pd.DataFrame(resultados)


def generar_graficos(df):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('CloudCore SaaS — ISO 22301: Análisis de Continuidad del Negocio', fontsize=13, fontweight='bold')


    # RTO Real vs Objetivo
    x = range(len(df))
    axes[0,0].barh(df['escenario'], df['rto_real_h'],
                   color=['#27ae60' if c else '#c0392b' for c in df['cumple_rto']])
    axes[0,0].axvline(RTO_OBJETIVO, color='navy', linestyle='--', label=f'RTO Obj={RTO_OBJETIVO}h')
    axes[0,0].set_title('RTO Real vs Objetivo (horas)')
    axes[0,0].legend()


    # Impacto financiero
    axes[0,1].bar(df['id'], df['impacto_financiero_usd'], color='#e74c3c', alpha=0.8)
    axes[0,1].set_title('Impacto Financiero por Escenario (USD)')
    axes[0,1].set_ylabel('USD')
    axes[0,1].tick_params(axis='x', rotation=30)


    # Riesgo residual
    axes[1,0].bar(df['id'], df['riesgo_residual_usd'], color='#8e44ad', alpha=0.8)
    axes[1,0].set_title('Riesgo Residual Anualizado (USD)')
    axes[1,0].set_ylabel('USD')
    axes[1,0].tick_params(axis='x', rotation=30)


    # Matriz riesgo: probabilidad vs impacto
    colores_scatter = ['#c0392b' if not c else '#27ae60' for c in df['cumple_rto']]
    axes[1,1].scatter(df['probabilidad'], df['impacto_financiero_usd']/1000,
                      s=df['clientes_impactados']/10, c=colores_scatter, alpha=0.7)
    for _, row in df.iterrows():
        axes[1,1].annotate(row['id'], (row['probabilidad'], row['impacto_financiero_usd']/1000), fontsize=8)
    axes[1,1].set_title('Matriz: Probabilidad vs Impacto (K USD)')
    axes[1,1].set_xlabel('Probabilidad')
    axes[1,1].set_ylabel('Impacto (K USD)')


    plt.tight_layout()
    ruta = f'{OUTPUT_DIR}/graficos/dia4_continuidad.png'
    plt.savefig(ruta, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'✅ Gráfico guardado: {ruta}')


if __name__ == '__main__':
    print('=' * 60)
    print('CloudCore SaaS — ISO 22301 | Continuidad del Negocio')
    print('=' * 60)
    df = analizar_escenarios()
    print(df[['id','escenario','rto_real_h','cumple_rto','impacto_financiero_usd','riesgo_residual_usd']].to_string(index=False))
    generar_graficos(df)
    df.to_csv(f'{OUTPUT_DIR}/reportes/dia4_continuidad.csv', index=False)
    print(f'\n💰 Impacto total: USD {df["impacto_financiero_usd"].sum():,.2f}')
    print(f'⚠️  Riesgo residual: USD {df["riesgo_residual_usd"].sum():,.2f}')
    rto_incumplen = df[~df['cumple_rto']]['escenario'].tolist()
    print(f'🚨 Escenarios que incumplen RTO: {rto_incumplen}')
    print('\n✅ Día 4 completado.')



