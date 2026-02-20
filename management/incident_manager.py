"""
CloudCore SaaS — management/incident_manager.py
ITIL 4: Gestor del ciclo de vida de incidentes
"""
import random
import logging
from datetime import datetime, timedelta
from domain.incident import Incident, Severity

logger = logging.getLogger(__name__)

INCIDENT_TYPES = [
    "Caída base de datos",
    "Falla de autenticación",
    "Timeout en facturación",
    "Error de sincronización",
    "Sobrecarga de CPU",
    "Falla de red CDN",
    "Error en API REST",
    "Falla de backup",
    "Certificado SSL expirado",
    "Corrupción de datos",
]

TEAMS = ["Equipo Alpha", "Equipo Beta", "Equipo Gamma"]


class IncidentManager:
    """
    Gestiona el ciclo de vida completo de los incidentes de CloudCore SaaS.
    Implementa las prácticas de Incident Management de ITIL 4 (AXELOS, 2019).
    """

    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.incidents: list[Incident] = []
        self._counter = 1

    def _next_id(self) -> str:
        iid = f"INC-2024-{self._counter:03d}"
        self._counter += 1
        return iid

    def register_incident(self, service_name: str, severity: Severity,
                          incident_type: str = None, team: str = None,
                          clients_affected: int = 0) -> Incident:
        """Registra un nuevo incidente en el sistema."""
        inc = Incident(
            incident_id=self._next_id(),
            service_name=service_name,
            severity=severity,
            incident_type=incident_type or random.choice(INCIDENT_TYPES),
            team=team or random.choice(TEAMS),
            clients_affected=clients_affected,
        )
        self.incidents.append(inc)
        logger.info(f"[INCIDENT REGISTERED] {inc.incident_id} | {inc.severity.name} | {inc.incident_type}")
        return inc

    def simulate_incidents(self, count: int = 10) -> list[Incident]:
        """
        Simula un lote de incidentes con resolución automática.
        Garantiza al menos 10 incidentes con variación realista.
        """
        severities   = [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]
        weights      = [0.10, 0.25, 0.35, 0.30]
        base_time    = datetime(2024, 1, 1, 8, 0, 0)

        for _ in range(count):
            sev  = random.choices(severities, weights=weights)[0]
            inc  = self.register_incident(
                service_name="CloudCore Facturación SaaS",
                severity=sev,
                clients_affected=random.randint(50, 3000) if sev == Severity.CRITICAL
                                 else random.randint(1, 500),
            )
            # Ajustar tiempos de creación y resolución
            offset_h = random.randint(1, 700)
            inc.created_at = base_time + timedelta(hours=offset_h)

            sla_h = inc.sla_limit_hours()
            # 30% de incidentes exceden el SLA (escenario realista)
            if random.random() < 0.30:
                factor = random.uniform(1.1, 3.0)
            else:
                factor = random.uniform(0.3, 0.95)

            resolution_h = sla_h * factor
            inc.resolve(inc.created_at + timedelta(hours=resolution_h))

        logger.info(f"[SIMULATION] {count} incidentes generados.")
        return self.incidents

    def get_open_incidents(self) -> list[Incident]:
        from domain.incident import IncidentStatus
        return [i for i in self.incidents if i.status == IncidentStatus.OPEN]

    def get_by_severity(self, severity: Severity) -> list[Incident]:
        return [i for i in self.incidents if i.severity == severity]

    def total_penalty_usd(self) -> float:
        return round(sum(i.penalty_usd() for i in self.incidents), 2)
