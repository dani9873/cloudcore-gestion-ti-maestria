"""
CloudCore SaaS — domain/service.py
ISO/IEC 20000: Entidad de dominio para Servicios TI
"""
from datetime import datetime
from enum import Enum


class ServiceStatus(Enum):
    OPERATIONAL  = "Operacional"
    DEGRADED     = "Degradado"
    OUTAGE       = "Fuera de servicio"
    MAINTENANCE  = "En mantenimiento"


class Service:
    """
    Representa un servicio TI crítico de CloudCore SaaS.
    Alineado con el catálogo de servicios de ISO/IEC 20000:2018.
    """

    COST_PER_HOUR_USD = 15000  # Costo de indisponibilidad por hora

    def __init__(self, service_id: str, name: str, tier: int,
                 sla_availability_pct: float = 99.9):
        self.service_id           = service_id
        self.name                 = name
        self.tier                 = tier          # 1=Crítico, 2=Importante, 3=Estándar
        self.sla_availability_pct = sla_availability_pct
        self.status               = ServiceStatus.OPERATIONAL
        self.downtime_events      = []            # Lista de eventos de inactividad

    def register_downtime(self, start: datetime, end: datetime, cause: str = ""):
        """Registra un evento de inactividad del servicio."""
        duration_h = (end - start).total_seconds() / 3600
        self.downtime_events.append({
            "start":       start.isoformat(),
            "end":         end.isoformat(),
            "duration_h":  round(duration_h, 4),
            "cause":       cause,
            "cost_usd":    round(duration_h * self.COST_PER_HOUR_USD, 2),
        })

    def total_downtime_hours(self) -> float:
        """Total de horas de inactividad registradas."""
        return sum(e["duration_h"] for e in self.downtime_events)

    def availability(self, total_hours: float) -> float:
        """Calcula el porcentaje de disponibilidad para el período dado."""
        if total_hours == 0:
            return 100.0
        uptime = total_hours - self.total_downtime_hours()
        return round((uptime / total_hours) * 100, 4)

    def meets_sla(self, total_hours: float) -> bool:
        """Determina si el servicio cumple el SLA de disponibilidad."""
        return self.availability(total_hours) >= self.sla_availability_pct

    def total_financial_impact(self) -> float:
        """Impacto financiero total acumulado por inactividad."""
        return round(sum(e["cost_usd"] for e in self.downtime_events), 2)

    def set_status(self, status: ServiceStatus):
        self.status = status

    def to_dict(self) -> dict:
        return {
            "service_id":           self.service_id,
            "name":                 self.name,
            "tier":                 self.tier,
            "sla_availability_pct": self.sla_availability_pct,
            "status":               self.status.value,
            "total_downtime_h":     round(self.total_downtime_hours(), 4),
            "total_cost_usd":       self.total_financial_impact(),
            "downtime_events":      self.downtime_events,
        }

    def __repr__(self):
        return f"<Service {self.service_id} | {self.name} | Tier {self.tier} | {self.status.value}>"
