"""
CloudCore SaaS — domain/risk.py
COBIT 2019 / ISO 31000: Entidad de dominio para Riesgo Operativo
"""
from enum import Enum


class RiskLevel(Enum):
    LOW      = "Bajo"
    MEDIUM   = "Medio"
    HIGH     = "Alto"
    CRITICAL = "Crítico"


class Risk:
    """
    Representa un riesgo operativo identificado en CloudCore SaaS.
    Basado en el marco de gestión de riesgos de COBIT 2019 (ISACA, 2019).
    """

    # Apetito de riesgo organizacional de CloudCore SaaS
    RISK_APPETITE_USD = 50_000  # Máximo riesgo residual anual tolerable

    def __init__(self, risk_id: str, name: str, category: str,
                 probability: float, impact_usd: float):
        """
        Args:
            probability: Probabilidad anual de ocurrencia (0.0 - 1.0)
            impact_usd:  Impacto financiero estimado en USD si ocurre
        """
        self.risk_id     = risk_id
        self.name        = name
        self.category    = category
        self.probability = probability
        self.impact_usd  = impact_usd
        self.controls    = []   # Controles mitigantes aplicados

    def inherent_risk_usd(self) -> float:
        """Riesgo inherente = Probabilidad × Impacto (sin controles)."""
        return round(self.probability * self.impact_usd, 2)

    def add_control(self, control_name: str, effectiveness: float):
        """
        Agrega un control mitigante.
        effectiveness: reducción del riesgo (0.0 - 1.0)
        """
        self.controls.append({
            "name":          control_name,
            "effectiveness": effectiveness,
        })

    def control_effectiveness(self) -> float:
        """Efectividad total combinada de todos los controles."""
        if not self.controls:
            return 0.0
        # Efectividad combinada (no acumulativa simple)
        remaining = 1.0
        for c in self.controls:
            remaining *= (1 - c["effectiveness"])
        return round(1 - remaining, 4)

    def residual_risk_usd(self) -> float:
        """Riesgo residual = Riesgo inherente × (1 - efectividad controles)."""
        reduction = self.control_effectiveness()
        return round(self.inherent_risk_usd() * (1 - reduction), 2)

    def risk_level(self) -> RiskLevel:
        """Clasifica el nivel de riesgo residual."""
        r = self.residual_risk_usd()
        if r < 10_000:
            return RiskLevel.LOW
        elif r < 30_000:
            return RiskLevel.MEDIUM
        elif r < 60_000:
            return RiskLevel.HIGH
        return RiskLevel.CRITICAL

    def exceeds_appetite(self) -> bool:
        """Determina si el riesgo residual supera el apetito organizacional."""
        return self.residual_risk_usd() > self.RISK_APPETITE_USD

    def to_dict(self) -> dict:
        return {
            "risk_id":          self.risk_id,
            "name":             self.name,
            "category":         self.category,
            "probability":      self.probability,
            "impact_usd":       self.impact_usd,
            "inherent_risk_usd": self.inherent_risk_usd(),
            "controls":         self.controls,
            "control_effectiveness": self.control_effectiveness(),
            "residual_risk_usd": self.residual_risk_usd(),
            "risk_level":       self.risk_level().value,
            "exceeds_appetite": self.exceeds_appetite(),
        }

    def __repr__(self):
        return (f"<Risk {self.risk_id} | {self.name} | "
                f"Residual: USD {self.residual_risk_usd():,.0f} | "
                f"{self.risk_level().value}>")
