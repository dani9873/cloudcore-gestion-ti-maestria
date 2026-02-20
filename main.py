"""
CloudCore SaaS — main.py
MODELO INTEGRADO: ITIL 4 + ISO/IEC 20000 + COBIT 2019 + ISO 22301
Tarea Semana 5 — Maestría en Gestión de Tecnologías de la Información
Universidad Mariano Gálvez de Guatemala
Curso: Planeación para la Continuidad del Negocio
"""
import logging
import os
import random
import time
import numpy as np
from datetime import datetime

# ── Configuración de logging estructurado ────────────────────────────────────
LOG_DIR = os.path.join(os.path.expanduser("~"), "cloudcore_saas", "outputs", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/cloudcore_main.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("CloudCore.Main")

# ── Imports del proyecto ─────────────────────────────────────────────────────
from domain.incident           import Incident, Severity
from domain.service            import Service, ServiceStatus
from domain.risk               import Risk
from domain.continuity         import ContinuityScenario, DisruptionType
from management.incident_manager    import IncidentManager
from management.sla_manager         import SLAManager
from management.availability_manager import AvailabilityManager
from governance.kpi            import KPI
from governance.cobit_dashboard import GovernanceDashboard
from continuity.recovery_simulator  import RecoverySimulator
from reports.report_generator  import ReportGenerator


def main():
    random.seed(42)
    np.random.seed(42)

    logger.info("=" * 60)
    logger.info("CloudCore SaaS — Sistema Integrado de Gestión TI")
    logger.info("Iniciando simulación completa...")
    logger.info("=" * 60)

    # ══════════════════════════════════════════════════════════
    # MÓDULO 1 — DÍA 1: ITIL 4 | Gestión de Incidentes
    # ══════════════════════════════════════════════════════════
    logger.info("\n[MÓDULO 1] ITIL 4 — Gestión de Incidentes y SLA")

    # Demostración código base del profesor
    incident_demo = Incident("INC-DEMO-001", "Facturacion SaaS", Severity.HIGH,
                             "Demo", "Equipo Alpha", 100)
    time.sleep(0.05)
    incident_demo.resolve()
    sla_demo = SLAManager()
    print("Demo SLA:", sla_demo.evaluate(incident_demo))

    # Simulación de 15 incidentes (cumple requisito ≥ 10)
    manager = IncidentManager(seed=42)
    incidents = manager.simulate_incidents(count=15)

    sla_mgr = SLAManager()
    sla_summary = sla_mgr.evaluate_batch(incidents)
    breakdown   = sla_mgr.compliance_by_severity(incidents)

    print(f"\n{'─'*55}")
    print("  ITIL 4 — Resultados de Gestión de Incidentes")
    print(f"{'─'*55}")
    print(f"  Total incidentes:     {sla_summary['total_incidents']}")
    print(f"  Cumplen SLA:          {sla_summary['compliant']}")
    print(f"  Tasa cumplimiento:    {sla_summary['compliance_rate_pct']:.2f}%")
    print(f"  Penalización total:   USD {sla_summary['total_penalty_usd']:,.2f}")
    print(f"  Estado SLA global:    {sla_summary['sla_status']}")
    print(f"{'─'*55}")
    print("  Desglose por severidad:")
    for sev, data in breakdown.items():
        print(f"    {sev}: {data['compliant']}/{data['total']} cumplen "
              f"({data['pct']:.1f}%) | Penalización: USD {data['penalty_usd']:,.2f}")

    reporter = ReportGenerator()
    reporter.save_structured_log("ITIL4_Incidentes", {
        "total_incidentes": sla_summary["total_incidents"],
        "tasa_cumplimiento_sla": sla_summary["compliance_rate_pct"],
        "penalizacion_total_usd": sla_summary["total_penalty_usd"],
        "desglose_severidad": breakdown,
        "estado_sla": sla_summary["sla_status"],
    })

    # ══════════════════════════════════════════════════════════
    # MÓDULO 2 — DÍA 2: ISO/IEC 20000 | Disponibilidad
    # ══════════════════════════════════════════════════════════
    logger.info("\n[MÓDULO 2] ISO/IEC 20000 — Disponibilidad del Servicio")

    # Demostración código base del profesor
    avail_demo = AvailabilityManager(total_minutes_period=43200)  # 30 días
    avail_demo.register_downtime(120)
    print(f"\nDemo Disponibilidad: {avail_demo.calculate_availability():.4f}%")

    avail_mgr = AvailabilityManager()
    MESES     = ["Ene","Feb","Mar","Abr","May","Jun",
                 "Jul","Ago","Sep","Oct","Nov","Dic"]
    # Datos simulados con meses críticos en Mar, Ago, Nov
    uptimes = np.random.uniform(99.85, 99.99, 12)
    uptimes[2]  = 99.38  # Marzo
    uptimes[4]  = 99.87
    uptimes[5]  = 99.87
    uptimes[6]  = 99.86
    uptimes[7]  = 99.54  # Agosto
    uptimes[10] = 98.52  # Noviembre

    HOURS_MONTH = 730
    for i, mes in enumerate(MESES):
        hours_down = HOURS_MONTH * (1 - uptimes[i] / 100)
        avail_mgr.record_monthly_availability(mes, uptimes[i], hours_down)

    availability_summary = avail_mgr.annual_summary()

    print(f"\n{'─'*55}")
    print("  ISO/IEC 20000 — Disponibilidad Anual")
    print(f"{'─'*55}")
    print(f"  Uptime anual promedio: {availability_summary['avg_annual_uptime_pct']:.4f}%")
    print(f"  Meses que cumplen:     {availability_summary['months_compliant']}/12")
    print(f"  Meses críticos:        {availability_summary['non_compliant_months']}")
    print(f"  Impacto financiero:    USD {availability_summary['total_financial_impact']:,.2f}")
    print(f"  Estado global:         {availability_summary['global_status']}")

    reporter.save_structured_log("ISO20000_Disponibilidad", availability_summary)

    # ══════════════════════════════════════════════════════════
    # MÓDULO 3 — DÍA 3: COBIT 2019 | Gobernanza y KPIs
    # ══════════════════════════════════════════════════════════
    logger.info("\n[MÓDULO 3] COBIT 2019 — Gobernanza y KPIs Estratégicos")

    dashboard = GovernanceDashboard(period="2024")

    dashboard.add_kpi(KPI("Disponibilidad",        availability_summary["avg_annual_uptime_pct"], 99.9,   "%", "ISO 20000"))
    dashboard.add_kpi(KPI("Cumplimiento SLA",       sla_summary["compliance_rate_pct"],           90.0,   "%", "ITIL 4"))
    dashboard.add_kpi(KPI("Incidentes Críticos",    0,                                             2,      "u", "ITIL 4", higher_is_better=False))
    dashboard.add_kpi(KPI("RTO Cumplimiento",       60.0,                                          60.0,   "%", "ISO 22301"))
    dashboard.add_kpi(KPI("Satisfacción Cliente",   82.3,                                          80.0,   "%", "COBIT 2019"))

    dashboard.summary()

    # Riesgos operativos con apetito de riesgo
    logger.info("\n[RIESGO OPERATIVO] Calculando riesgo residual...")
    risks = [
        Risk("RSK-001", "Indisponibilidad por incidentes P1/P2", "Operacional", 0.35, 120_000),
        Risk("RSK-002", "Ransomware",                            "Ciberseguridad", 0.08, 295_000),
        Risk("RSK-003", "Fallo de base de datos",                "Infraestructura", 0.15, 60_000),
        Risk("RSK-004", "Incumplimiento regulatorio",            "Cumplimiento",    0.10, 200_000),
    ]
    risks[0].add_control("Monitoreo 24/7",         effectiveness=0.40)
    risks[1].add_control("Backup offline inmutable", effectiveness=0.55)
    risks[2].add_control("Réplica activo-activo",   effectiveness=0.60)
    risks[3].add_control("Auditoría trimestral",    effectiveness=0.30)

    print(f"\n{'─'*55}")
    print("  Riesgo Operativo — Apetito de Riesgo: USD 50,000")
    print(f"{'─'*55}")
    total_residual = 0
    for r in risks:
        flag = "⚠ EXCEDE APETITO" if r.exceeds_appetite() else "✓ Dentro del apetito"
        print(f"  {r.risk_id} | {r.name}")
        print(f"    Inherente: USD {r.inherent_risk_usd():>10,.2f} | "
              f"Residual: USD {r.residual_risk_usd():>10,.2f} | {flag}")
        total_residual += r.residual_risk_usd()
    print(f"{'─'*55}")
    print(f"  Riesgo residual total: USD {total_residual:,.2f}")

    dashboard_data = dashboard.to_dict()
    reporter.save_structured_log("COBIT2019_Gobernanza", dashboard_data)

    # ══════════════════════════════════════════════════════════
    # MÓDULO 4 — DÍA 4: ISO 22301 | Continuidad del Negocio
    # ══════════════════════════════════════════════════════════
    logger.info("\n[MÓDULO 4] ISO 22301 — Continuidad del Negocio")

    # Demostración código base del profesor
    recovery_demo = RecoverySimulator(rto_minutes=60)
    print(f"\nDemo Recuperación (45 min): {recovery_demo.simulate_recovery(45)}")
    print(f"Demo Recuperación (90 min): {recovery_demo.simulate_recovery(90)}")

    simulator = RecoverySimulator(rto_hours=4.0)
    for scenario in RecoverySimulator.default_scenarios(seed=42):
        simulator.add_scenario(scenario)

    results  = simulator.run_all()
    cont_sum = simulator.continuity_summary()

    print(f"\n{'─'*55}")
    print("  ISO 22301 — Análisis de Continuidad")
    print(f"{'─'*55}")
    for r in results:
        rto_s = "✓" if r["meets_rto"] else "✗"
        rpo_s = "✓" if r["meets_rpo"] else "✗"
        print(f"  {r['scenario_id']} | {r['disruption_type']}")
        print(f"    RTO: {r['actual_rto_h']:.2f}h {rto_s} | RPO: {r['actual_rpo_h']:.2f}h {rpo_s} | "
              f"Impacto: USD {r['financial_impact_usd']:,.2f}")
    print(f"{'─'*55}")
    print(f"  RTO cumplimiento: {cont_sum['rto_compliance_pct']:.1f}%")
    print(f"  Escenarios críticos: {cont_sum['critical_scenarios']}")
    print(f"  Impacto total: USD {cont_sum['total_financial_impact_usd']:,.2f}")

    reporter.save_structured_log("ISO22301_Continuidad", cont_sum)

    # ══════════════════════════════════════════════════════════
    # MÓDULO 5 — DÍA 5: INFORME FINAL INTEGRADO
    # ══════════════════════════════════════════════════════════
    logger.info("\n[MÓDULO 5] Generando Informe Ejecutivo Final Integrado...")

    reporter.generate_final_report(
        sla_summary          = sla_summary,
        availability_summary = availability_summary,
        dashboard_data       = dashboard_data,
        continuity_summary   = cont_sum,
    )

    logger.info("=" * 60)
    logger.info("✅ Simulación completada. Todos los módulos ejecutados.")
    logger.info(f"   Outputs en: ~/cloudcore_saas/outputs/")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
