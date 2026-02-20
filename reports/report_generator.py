"""
CloudCore SaaS — reports/report_generator.py
Generador automático de reportes en texto estructurado y JSON
"""
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "cloudcore_saas", "outputs")


class ReportGenerator:
    """
    Genera informes ejecutivos automáticos en texto estructurado y JSON.
    Consolida resultados de los cuatro marcos de referencia.
    """

    def __init__(self):
        os.makedirs(f"{OUTPUT_DIR}/reportes", exist_ok=True)
        os.makedirs(f"{OUTPUT_DIR}/logs",     exist_ok=True)

    def _save_json(self, data: dict, filename: str):
        path = f"{OUTPUT_DIR}/logs/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        logger.info(f"[REPORT] JSON guardado: {path}")
        return path

    def _save_text(self, content: str, filename: str):
        path = f"{OUTPUT_DIR}/reportes/{filename}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"[REPORT] Texto guardado: {path}")
        return path

    def generate_final_report(self, sla_summary: dict, availability_summary: dict,
                               dashboard_data: dict, continuity_summary: dict) -> str:
        """Genera el informe ejecutivo final integrado en texto estructurado."""
        now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = "=" * 65

        # Calcular madurez
        maturity_score = 0
        if availability_summary.get("avg_annual_uptime_pct", 0) >= 99.9: maturity_score += 1
        if sla_summary.get("compliance_rate_pct", 0) >= 90:               maturity_score += 1
        if dashboard_data.get("maturity_level", 0) >= 3:                  maturity_score += 1
        if continuity_summary.get("rto_compliance_pct", 0) >= 60:         maturity_score += 1
        if sla_summary.get("compliance_rate_pct", 0) >= 80:               maturity_score += 1

        maturity_descs = {5:"Optimizado",4:"Cuantitativamente Gestionado",
                          3:"Definido",2:"Gestionado",1:"Inicial",0:"Inexistente"}
        maturity_txt   = maturity_descs.get(maturity_score, "Inicial")

        report = f"""
{line}
   INFORME EJECUTIVO FINAL — CloudCore SaaS
   Sistema Integrado de Gestión TI
   Generado: {now}
   Marcos: ITIL 4 | ISO/IEC 20000 | COBIT 2019 | ISO 22301
{line}

1. RESUMEN EJECUTIVO
   CloudCore SaaS opera una plataforma crítica de facturación electrónica
   para 3,000 clientes empresariales con dependencia tecnológica del 100%.
   Nivel de Madurez Integrado: {maturity_score}/5 — {maturity_txt}

{line}
2. GESTIÓN DE INCIDENTES — ITIL 4
{line}
   Total incidentes:        {sla_summary.get('total_incidents', 0)}
   Cumplen SLA:             {sla_summary.get('compliant', 0)}
   Incumplen SLA:           {sla_summary.get('non_compliant', 0)}
   Tasa de cumplimiento:    {sla_summary.get('compliance_rate_pct', 0):.2f}%
   Penalización total:      USD {sla_summary.get('total_penalty_usd', 0):,.2f}
   Estado SLA:              {sla_summary.get('sla_status', 'N/A')}

{line}
3. DISPONIBILIDAD — ISO/IEC 20000
{line}
   Uptime anual promedio:   {availability_summary.get('avg_annual_uptime_pct', 0):.4f}%
   SLA objetivo:            99.9%
   Meses que cumplen SLA:   {availability_summary.get('months_compliant', 0)}/12
   Meses que incumplen:     {availability_summary.get('months_non_compliant', 0)}/12
   Meses críticos:          {availability_summary.get('non_compliant_months', [])}
   Impacto financiero:      USD {availability_summary.get('total_financial_impact', 0):,.2f}
   Estado global:           {availability_summary.get('global_status', 'N/A')}

{line}
4. GOBERNANZA TI — COBIT 2019
{line}
   KPIs evaluados:          {len(dashboard_data.get('kpis', []))}
   KPIs en ALERTA:          {dashboard_data.get('alerts_count', 0)}
   Estado de Gobernanza:    {dashboard_data.get('governance_status', 'N/A')}
   Madurez COBIT:           {dashboard_data.get('maturity_level', 0)}/5 — {dashboard_data.get('maturity_desc', 'N/A')}

   Decisiones del Comité:"""
        for dec in dashboard_data.get("committee_decisions", []):
            report += f"\n   • {dec}"

        report += f"""

{line}
5. CONTINUIDAD DEL NEGOCIO — ISO 22301
{line}
   Escenarios evaluados:    {continuity_summary.get('total_scenarios', 0)}
   Cumplen RTO (≤4h):       {continuity_summary.get('rto_compliant', 0)} ({continuity_summary.get('rto_compliance_pct', 0):.1f}%)
   Cumplen RPO (≤15min):    {continuity_summary.get('rpo_compliant', 0)} ({continuity_summary.get('rpo_compliance_pct', 0):.1f}%)
   Escenarios críticos:     {continuity_summary.get('critical_scenarios', [])}
   Impacto financiero:      USD {continuity_summary.get('total_financial_impact_usd', 0):,.2f}
   Riesgo residual total:   USD {continuity_summary.get('total_residual_risk_usd', 0):,.2f}

{line}
6. EVALUACIÓN DE MADUREZ INTEGRADA
{line}
   Nivel alcanzado:  {maturity_score}/5 — {maturity_txt}

   Criterios evaluados:
   [{'✓' if availability_summary.get('avg_annual_uptime_pct',0)>=99.9 else '✗'}] Disponibilidad anual ≥ 99.9%
   [{'✓' if sla_summary.get('compliance_rate_pct',0)>=90 else '✗'}] Cumplimiento SLA incidentes ≥ 90%
   [{'✓' if dashboard_data.get('maturity_level',0)>=3 else '✗'}] Madurez COBIT ≥ Nivel 3
   [{'✓' if continuity_summary.get('rto_compliance_pct',0)>=60 else '✗'}] RTO cumplimiento ≥ 60%
   [{'✓' if sla_summary.get('compliance_rate_pct',0)>=80 else '✗'}] Satisfacción/SLA operativo ≥ 80%

{line}
7. RECOMENDACIONES ESTRATÉGICAS
{line}
   1. Implementar monitoreo proactivo 24/7 con alertas automatizadas P1/P2.
   2. Establecer replicación geográfica activo-activo para la base de datos.
   3. Actualizar el DRP con procedimientos específicos contra ransomware.
   4. Formalizar comité de continuidad con reuniones quincenales y KPIs.
   5. Implementar chaos engineering mensual para validar RTO en staging.
   6. Certificar el SMS bajo ISO/IEC 20000 para diferenciación competitiva.
   7. Capacitar y certificar el equipo ITSM en ITIL Foundation.

{line}
   Repositorio del proyecto:
   https://github.com/dani9873/cloudcore-gestion-ti-maestria
{line}
"""
        self._save_text(report, "informe_final_integrado.txt")
        self._save_json({
            "timestamp": datetime.now().isoformat(),
            "sla": sla_summary,
            "availability": availability_summary,
            "governance": dashboard_data,
            "continuity": continuity_summary,
            "maturity_score": maturity_score,
            "maturity_desc": maturity_txt,
        }, "informe_final_integrado.json")

        print(report)
        return report

    def save_structured_log(self, module: str, data: dict):
        """Guarda un log estructurado en JSON para un módulo específico."""
        payload = {
            "timestamp": datetime.now().isoformat(),
            "module":    module,
            "empresa":   "CloudCore SaaS",
            **data,
        }
        self._save_json(payload, f"log_{module.lower().replace(' ', '_')}.json")
