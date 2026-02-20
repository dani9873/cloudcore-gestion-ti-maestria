"""
CloudCore SaaS — domain/continuity.py
ISO 22301:2019: Entidad de dominio para Continuidad del Negocio
"""
from enum import Enum


class DisruptionType(Enum):
    DATABASE_FAILURE  = "Fallo Total de Base de Datos"
    RANSOMWARE        = "Ataque Ransomware"
    CLOUD_OUTAGE      = "Caída de Infraestructura Cloud"
    NETWORK_LOSS      = "Pérdida de Conectividad de Red"
    DEPLOY_FAILURE    = "Error Crítico en Despliegue"


class ContinuityScenario:
    """
    Representa un escenario de interrupción del negocio para CloudCore SaaS.
    Basado en el estándar ISO 22301:2019 (ISO, 2019).
    """

    COST_PER_HOUR_USD = 15_000   # Impacto financiero por hora de inactividad

    def __init__(self, scenario_id: str, disruption_type: DisruptionType,
                 probability: float, rto_objective_h: float,
                 rpo_objective_h: float, clients_affected: int):
        """
        Args:
            rto_objective_h: Recovery Time Objective en horas
            rpo_objective_h: Recovery Point Objective en horas
            probability:     Probabilidad anual de ocurrencia (0.0–1.0)
        """
        self.scenario_id       = scenario_id
        self.disruption_type   = disruption_type
        self.probability       = probability
        self.rto_objective_h   = rto_objective_h
        self.rpo_objective_h   = rpo_objective_h
        self.clients_affected  = clients_affected
        self.actual_rto_h      = None
        self.actual_rpo_h      = None

    def simulate(self, actual_rto_h: float, actual_rpo_h: float):
        """Registra los tiempos reales de recuperación de la simulación."""
        self.actual_rto_h = actual_rto_h
        self.actual_rpo_h = actual_rpo_h

    def meets_rto(self) -> bool:
        if self.actual_rto_h is None:
            return False
        return self.actual_rto_h <= self.rto_objective_h

    def meets_rpo(self) -> bool:
        if self.actual_rpo_h is None:
            return False
        return self.actual_rpo_h <= self.rpo_objective_h

    def financial_impact_usd(self) -> float:
        """Impacto financiero estimado basado en el RTO real."""
        if self.actual_rto_h is None:
            return 0.0
        return round(self.actual_rto_h * self.COST_PER_HOUR_USD, 2)

    def residual_risk_usd(self) -> float:
        """Riesgo residual anualizado = Probabilidad × Impacto."""
        return round(self.probability * self.financial_impact_usd(), 2)

    def rto_gap_h(self) -> float:
        """Brecha entre RTO real y objetivo (positivo = incumplimiento)."""
        if self.actual_rto_h is None:
            return 0.0
        return round(max(0.0, self.actual_rto_h - self.rto_objective_h), 2)

    def to_dict(self) -> dict:
        return {
            "scenario_id":        self.scenario_id,
            "disruption_type":    self.disruption_type.value,
            "probability":        self.probability,
            "rto_objective_h":    self.rto_objective_h,
            "rpo_objective_h":    self.rpo_objective_h,
            "actual_rto_h":       self.actual_rto_h,
            "actual_rpo_h":       self.actual_rpo_h,
            "meets_rto":          self.meets_rto(),
            "meets_rpo":          self.meets_rpo(),
            "rto_gap_h":          self.rto_gap_h(),
            "clients_affected":   self.clients_affected,
            "financial_impact_usd": self.financial_impact_usd(),
            "residual_risk_usd":  self.residual_risk_usd(),
        }

    def __repr__(self):
        status = "✓ RTO OK" if self.meets_rto() else f"✗ RTO +{self.rto_gap_h():.1f}h"
        return f"<Scenario {self.scenario_id} | {self.disruption_type.value} | {status}>"
