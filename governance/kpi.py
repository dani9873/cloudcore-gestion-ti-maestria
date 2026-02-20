"""
CloudCore SaaS — governance/kpi.py
COBIT 2019: Indicadores Clave de Desempeño para Gobernanza TI
"""
import logging

logger = logging.getLogger(__name__)


class KPI:
    """
    Indicador Clave de Desempeño para el comité de gobernanza TI.
    Alineado con la cascada de metas de COBIT 2019 (ISACA, 2019).
    """

    def __init__(self, name: str, value: float, threshold: float,
                 unit: str = "%", framework: str = "COBIT 2019",
                 higher_is_better: bool = True):
        self.name             = name
        self.value            = value
        self.threshold        = threshold
        self.unit             = unit
        self.framework        = framework
        self.higher_is_better = higher_is_better

    def status(self) -> str:
        """Retorna el estado del KPI respecto al umbral."""
        if self.higher_is_better:
            return "OK" if self.value >= self.threshold else "ALERTA"
        else:
            return "OK" if self.value <= self.threshold else "ALERTA"

    def gap(self) -> float:
        """Brecha entre el valor actual y el umbral objetivo."""
        return round(self.value - self.threshold, 4)

    def gap_pct(self) -> float:
        """Brecha como porcentaje del umbral."""
        if self.threshold == 0:
            return 0.0
        return round((self.gap() / self.threshold) * 100, 2)

    def to_dict(self) -> dict:
        return {
            "name":      self.name,
            "value":     self.value,
            "threshold": self.threshold,
            "unit":      self.unit,
            "framework": self.framework,
            "status":    self.status(),
            "gap":       self.gap(),
        }

    def __repr__(self):
        return f"<KPI '{self.name}' | {self.value}{self.unit} vs {self.threshold}{self.unit} | {self.status()}>"
