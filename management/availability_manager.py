"""
CloudCore SaaS — management/availability_manager.py
ISO/IEC 20000:2018: Gestor de Disponibilidad del Servicio
"""
import logging
from datetime import datetime
from domain.service import Service

logger = logging.getLogger(__name__)


class AvailabilityManager:
    """
    Gestiona el monitoreo y cálculo de disponibilidad de servicios TI.
    Alineado con los requisitos de gestión de disponibilidad de ISO/IEC 20000:2018.
    """

    HOURS_PER_MONTH = 730  # Promedio de horas por mes

    def __init__(self, total_minutes_period: int = None):
        # Compatible con el código base del profesor
        self.total_minutes = total_minutes_period or (self.HOURS_PER_MONTH * 60 * 12)
        self.downtime_minutes = 0
        self.services: list[Service] = []
        self.monthly_records: list[dict] = []

    def register_downtime(self, minutes: float):
        """Registra downtime directo en minutos (compatible con código base)."""
        self.downtime_minutes += minutes

    def calculate_availability(self) -> float:
        """Calcula disponibilidad del período total."""
        uptime = self.total_minutes - self.downtime_minutes
        return round((uptime / self.total_minutes) * 100, 4)

    def evaluate_sla(self, target: float = 99.9) -> bool:
        """Evalúa si la disponibilidad cumple el SLA objetivo."""
        return self.calculate_availability() >= target

    def add_service(self, service: Service):
        """Agrega un servicio al monitoreo."""
        self.services.append(service)

    def record_monthly_availability(self, month: str, uptime_pct: float,
                                    hours_down: float, sla_target: float = 99.9):
        """Registra disponibilidad mensual para análisis anual."""
        cost = round(hours_down * Service.COST_PER_HOUR_USD, 2)
        record = {
            "month":           month,
            "uptime_pct":      round(uptime_pct, 4),
            "hours_down":      round(hours_down, 2),
            "minutes_down":    round(hours_down * 60, 1),
            "meets_sla":       uptime_pct >= sla_target,
            "financial_impact": cost,
        }
        self.monthly_records.append(record)
        status = "✓" if record["meets_sla"] else "✗"
        logger.info(
            f"[AVAILABILITY] {month} | {uptime_pct:.4f}% | "
            f"Down: {hours_down:.2f}h | {status} SLA | Impact: USD {cost:,.2f}"
        )
        return record

    def annual_summary(self, sla_target: float = 99.9) -> dict:
        """Genera resumen anual de disponibilidad."""
        if not self.monthly_records:
            return {}
        avg_uptime = sum(r["uptime_pct"] for r in self.monthly_records) / len(self.monthly_records)
        compliant  = [r for r in self.monthly_records if r["meets_sla"]]
        total_cost = sum(r["financial_impact"] for r in self.monthly_records)

        summary = {
            "avg_annual_uptime_pct":  round(avg_uptime, 4),
            "months_compliant":       len(compliant),
            "months_non_compliant":   len(self.monthly_records) - len(compliant),
            "non_compliant_months":   [r["month"] for r in self.monthly_records if not r["meets_sla"]],
            "total_financial_impact": round(total_cost, 2),
            "global_status":          "CUMPLE" if avg_uptime >= sla_target else "REQUIERE_MEJORA",
        }
        logger.warning(
            f"[ANNUAL AVAILABILITY] Uptime: {avg_uptime:.4f}% | "
            f"Meses incumplidores: {summary['non_compliant_months']} | "
            f"Impacto total: USD {total_cost:,.2f}"
        )
        return summary
