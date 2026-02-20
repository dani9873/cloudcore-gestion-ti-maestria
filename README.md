# 🚀 CloudCore SaaS — Sistema Integrado de Gestión TI

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ITIL 4](https://img.shields.io/badge/Marco-ITIL%204-0052CC.svg)]()
[![ISO 20000](https://img.shields.io/badge/Marco-ISO%2FIEC%2020000-red.svg)]()
[![COBIT 2019](https://img.shields.io/badge/Marco-COBIT%202019-orange.svg)]()
[![ISO 22301](https://img.shields.io/badge/Marco-ISO%2022301-purple.svg)]()

> **Trabajo Semana 5 — Maestría en Gestión de Tecnologías de la Información**  
> Simulación computacional de gestión de servicios TI, disponibilidad, gobernanza y continuidad del negocio para una plataforma SaaS crítica de facturación electrónica.

---

## 📋 Descripción del Proyecto

Este repositorio contiene el sistema de simulación computacional desarrollado como caso de estudio para **CloudCore SaaS**, empresa proveedora de una plataforma crítica de facturación electrónica para **3,000 clientes empresariales** con dependencia tecnológica del 100%.

El sistema integra cuatro marcos de referencia internacionales:

| Marco | Versión | Módulo | Archivo |
|-------|---------|--------|---------|
| **ITIL 4** | AXELOS 2019 | Gestión de Incidentes y SLA | `src/dia1_itil/` |
| **ISO/IEC 20000** | ISO 2018 | Disponibilidad y Uptime | `src/dia2_iso20000/` |
| **COBIT 2019** | ISACA 2019 | Dashboard KPIs Estratégicos | `src/dia3_cobit/` |
| **ISO 22301** | ISO 2019 | Continuidad del Negocio / RTO | `src/dia4_iso22301/` |
| **Modelo Integrado** | — | Dashboard Unificado + PDF | `src/dia5_integrado/` |

---

## 📊 Resultados Obtenidos

| Indicador | Valor | Estado |
|-----------|-------|--------|
| Tasa cumplimiento SLA incidentes | 53,33% | 🔴 Incumple |
| Disponibilidad anual promedio | 99,728% | 🔴 Incumple (obj. 99,9%) |
| Meses que cumplen SLA disponibilidad | 6/12 | 🔴 Incumple |
| Impacto financiero anual (downtime) | USD 357,764.92 | — |
| Penalizaciones SLA incidentes | USD 51,431.48 | — |
| Escenarios que cumplen RTO | 3/5 | 🟡 Parcial |
| RTO ransomware (obj. < 4h) | 19,71 h | 🔴 Crítico |
| Nivel de Madurez COBIT 2019 | **1 / 5 — Inicial** | 🔴 Requiere mejora |

---

## 🗂️ Estructura del Repositorio

```
cloudcore-saas-itsm/
│
├── src/
│   ├── dia1_itil/
│   │   └── dia1_incidentes.py          # Gestión de incidentes ITIL 4
│   ├── dia2_iso20000/
│   │   └── dia2_disponibilidad.py      # Disponibilidad ISO/IEC 20000
│   ├── dia3_cobit/
│   │   └── dia3_cobit_dashboard.py     # KPIs y gobernanza COBIT 2019
│   ├── dia4_iso22301/
│   │   └── dia4_continuidad.py         # Continuidad del negocio ISO 22301
│   └── dia5_integrado/
│       └── dia5_modelo_integrado.py    # Modelo unificado + PDF automático
│
├── outputs/                            # Generado automáticamente (excluido de Git)
│   ├── reportes/                       # CSVs y JSONs de resultados
│   ├── graficos/                       # Dashboards PNG
│   ├── logs/                           # Logs estructurados JSON
│   └── pdf/                            # Informe ejecutivo PDF
│
├── docs/
│   └── evidencias/                     # Capturas de pantalla de ejecución
│
├── requirements.txt                    # Dependencias Python
├── .gitignore
├── LICENSE
└── README.md
```

---

## ⚙️ Requisitos del Sistema

- **Sistema Operativo:** Kali Linux 2024 / Ubuntu 22.04+ / Debian 12+
- **Python:** 3.10 o superior (probado en 3.13)
- **Git:** 2.x

---

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/dani9873/cloudcore-saas-itsm.git
cd cloudcore-saas-itsm
```

### 2. Crear y activar entorno virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ▶️ Ejecución

Ejecuta cada módulo de forma independiente o en secuencia:

```bash
# Día 1 — ITIL 4: Gestión de Incidentes
python3 src/dia1_itil/dia1_incidentes.py

# Día 2 — ISO/IEC 20000: Disponibilidad
python3 src/dia2_iso20000/dia2_disponibilidad.py

# Día 3 — COBIT 2019: Dashboard KPIs
python3 src/dia3_cobit/dia3_cobit_dashboard.py

# Día 4 — ISO 22301: Continuidad del Negocio
python3 src/dia4_iso22301/dia4_continuidad.py

# Día 5 — Modelo Integrado + PDF automático
python3 src/dia5_integrado/dia5_modelo_integrado.py
```

Los artefactos generados se guardan automáticamente en `outputs/`.

---

## 📦 Dependencias (`requirements.txt`)

```
pandas==2.2.2
numpy==1.26.4
matplotlib==3.8.4
seaborn==0.13.2
reportlab==4.1.0
```

---

## 👥 Equipo de Trabajo

| Rol | Responsabilidad |
|-----|----------------|
| Arquitecto de Servicios TI | Diseño del sistema, arquitectura de módulos |
| Responsable de Continuidad | Módulo ISO 22301, escenarios de crisis |
| Analista de Riesgos Operativos | Métricas de riesgo, riesgo residual |
| Especialista ITSM | Módulos ITIL 4 e ISO/IEC 20000 |
| Auditor / Gobernanza TI | Dashboard COBIT 2019, evaluación de madurez |

---

## 📚 Referencias

- AXELOS. (2019). *ITIL Foundation: ITIL 4 Edition*. TSO.
- ISO. (2018). *ISO/IEC 20000-1:2018 — Service management system requirements*. ISO.
- ISO. (2019). *ISO 22301:2019 — Business continuity management systems*. ISO.
- ISACA. (2019). *COBIT 2019 Framework: Introduction and Methodology*. ISACA.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia MIT. Ver archivo [LICENSE](LICENSE) para más detalles.

---

*Trabajo académico desarrollado para la Maestría en Gestión de Tecnologías de la Información — Semana 5, febrero 2026.*
