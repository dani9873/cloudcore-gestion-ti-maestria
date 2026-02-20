"""
CloudCore SaaS — domain/incident.py
ITIL 4: Entidad de dominio para Incidentes de Servicio
"""
from datetime import datetime
from enum import Enum


class Severity(Enum):
    CRITICAL = 1   # P1 - Sistema caído totalmente
    HIGH     = 2   # P2 - Funcionalidad mayor degradada
    MEDIUM   = 3   # P3 - Funcionalidad menor afectada
    LOW      = 4   # P4 - Consulta o mejora


class IncidentStatus(Enum):
    OPEN       = "Abierto"
    IN_PROGRESS = "En progreso"
    RESOLVED   = "Resuelto"
    CLOSED     = "Cerrado"


class Incident:
    """
    Representa un incidente de servicio en la plataforma CloudCore SaaS.
    Basado en la práctica de Gestión de Incidentes de ITIL 4 (AXELOS, 2019).
    """

    # SLA máximo de resolución en horas por severidad
    SLA_HOURS = {
        Severity.CRITICAL: 1,
        Severity.HIGH:     4,
        Severity.MEDIUM:   8,
        Severity.LOW:      24,
    }

    # Penalización en USD por hora de exceso según severidad
    PENALTY_USD_PER_HOUR = {
        Severity.CRITICAL: 5000,
        Severity.HIGH:     2000,
        Severity.MEDIUM:   500,
        Severity.LOW:      100,
    }

    def __init__(self, incident_id: str, service_name: str, severity: Severity,
                 incident_type: str, team: str, clients_affected: int = 0):
        self.incident_id      = incident_id
        self.service_name     = service_name
        self.severity         = severity
        self.incident_type    = incident_type
        self.team             = team
        self.clients_affected = clients_affected
        self.status           = IncidentStatus.OPEN
        self.created_at       = datetime.now()
        self.resolved_at      = None
        self.notes            = []

    def resolve(self, resolved_at: datetime = None):
        """Marca el incidente como resuelto."""
        self.resolved_at = resolved_at or datetime.now()
        self.status = IncidentStatus.RESOLVED

    def close(self):
        """Cierra el incidente formalmente."""
        self.status = IncidentStatus.CLOSED

    def add_note(self, note: str):
        """Agrega una nota de seguimiento al incidente."""
        self.notes.append({"timestamp": datetime.now().isoformat(), "note": note})

    def resolution_time_hours(self) -> float:
        """Calcula el tiempo de resolución en horas."""
        if self.resolved_at:
            delta = self.resolved_at - self.created_at
            return delta.total_seconds() / 3600
        return None

    def sla_limit_hours(self) -> int:
        """Retorna el SLA máximo de resolución según severidad."""
        return self.SLA_HOURS[self.severity]

    def meets_sla(self) -> bool:
        """Determina si el incidente fue resuelto dentro del SLA."""
        t = self.resolution_time_hours()
        if t is None:
            return False
        return t <= self.sla_limit_hours()

    def excess_hours(self) -> float:
        """Horas de exceso sobre el SLA (0 si cumple)."""
        t = self.resolution_time_hours()
        if t is None:
            return 0.0
        return max(0.0, t - self.sla_limit_hours())

    def penalty_usd(self) -> float:
        """Penalización en USD por incumplimiento SLA."""
        return round(self.excess_hours() * self.PENALTY_USD_PER_HOUR[self.severity], 2)

    def to_dict(self) -> dict:
        """Serializa el incidente a diccionario."""
        return {
            "incident_id":      self.incident_id,
            "service_name":     self.service_name,
            "severity":         self.severity.name,
            "incident_type":    self.incident_type,
            "team":             self.team,
            "clients_affected": self.clients_affected,
            "status":           self.status.value,
            "created_at":       self.created_at.isoformat(),
            "resolved_at":      self.resolved_at.isoformat() if self.resolved_at else None,
            "resolution_time_h": round(self.resolution_time_hours(), 4) if self.resolution_time_hours() else None,
            "sla_limit_h":      self.sla_limit_hours(),
            "meets_sla":        self.meets_sla(),
            "excess_h":         round(self.excess_hours(), 4),
            "penalty_usd":      self.penalty_usd(),
        }

    def __repr__(self):
        return (f"<Incident {self.incident_id} | {self.severity.name} | "
                f"{self.status.value} | SLA: {'✓' if self.meets_sla() else '✗'}>")
