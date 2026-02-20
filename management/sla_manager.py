"""
CloudCore SaaS — management/sla_manager.py
ITIL 4: Gestor de Acuerdos de Nivel de Servicio
"""
from domain.incident import Incident, Severity
import logging

logger = logging.getLogger(__name__)


class SLAManager:
    """
    Gestiona la evaluación y seguimiento de SLAs de incidentes.
    Basado en la práctica Service Level Management de ITIL 4 (AXELOS, 2019).
    """

    def __init__(self):
        self.evaluations = []

    def evaluate(self, incident: Incident) -> str:
        """Evalúa si un incidente cumple su SLA."""
        t = incident.resolution_time_hours()
        if t is None:
            return "Pendiente"
        result = "Cumple SLA" if incident.meets_sla() else "Incumple SLA"
        logger.info(
            f"[SLA] {incident.incident_id} | {incident.severity.name} | "
            f"Tiempo: {t:.2f}h | SLA: {incident.sla_limit_hours()}h | {result}"
        )
        self.evaluations.append({
            "incident_id": incident.incident_id,
            "severity":    incident.severity.name,
            "result":      result,
            "penalty_usd": incident.penalty_usd(),
        })
        return result

    def evaluate_batch(self, incidents: list) -> dict:
        """Evalúa una lista de incidentes y retorna resumen ejecutivo."""
        results = [self.evaluate(i) for i in incidents]
        total    = len(incidents)
        compliant = sum(1 for i in incidents if i.meets_sla())
        total_penalty = sum(i.penalty_usd() for i in incidents)

        summary = {
            "total_incidents":    total,
            "compliant":          compliant,
            "non_compliant":      total - compliant,
            "compliance_rate_pct": round(compliant / total * 100, 2) if total else 0,
            "total_penalty_usd":  round(total_penalty, 2),
            "sla_status":         "CUMPLE" if compliant / total >= 0.95 else "INCUMPLE",
        }
        logger.warning(
            f"[SLA BATCH] Cumplimiento: {summary['compliance_rate_pct']}% | "
            f"Penalización total: USD {summary['total_penalty_usd']:,.2f}"
        )
        return summary

    def compliance_by_severity(self, incidents: list) -> dict:
        """Desglosa el cumplimiento SLA por nivel de severidad."""
        from collections import defaultdict
        groups = defaultdict(list)
        for i in incidents:
            groups[i.severity.name].append(i)

        breakdown = {}
        for sev, group in groups.items():
            compliant = sum(1 for i in group if i.meets_sla())
            breakdown[sev] = {
                "total":          len(group),
                "compliant":      compliant,
                "pct":            round(compliant / len(group) * 100, 2),
                "penalty_usd":    round(sum(i.penalty_usd() for i in group), 2),
                "avg_time_h":     round(
                    sum(i.resolution_time_hours() for i in group if i.resolution_time_hours()) / len(group), 2
                ),
            }
        return breakdown
