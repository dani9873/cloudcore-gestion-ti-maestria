"""
CloudCore SaaS — governance/cobit_dashboard.py
COBIT 2019: Dashboard de Gobernanza TI — Dominio EDM
"""
import logging
from governance.kpi import KPI

logger = logging.getLogger(__name__)


class GovernanceDashboard:
    """
    Dashboard ejecutivo del comité de gobernanza TI de CloudCore SaaS.
    Basado en el dominio EDM (Evaluar, Dirigir, Monitorear) de COBIT 2019.
    """

    # Apetito de riesgo: máximo de KPIs en ALERTA tolerable
    MAX_ALERTS_TOLERATED = 1

    def __init__(self, period: str = "2024"):
        self.period  = period
        self.kpis: list[KPI] = []

    def add_kpi(self, kpi: KPI):
        """Agrega un KPI al dashboard."""
        self.kpis.append(kpi)
        logger.info(f"[COBIT KPI] {kpi.name}: {kpi.value}{kpi.unit} | {kpi.status()}")

    def summary(self):
        """Imprime el resumen ejecutivo del dashboard (compatible con código base)."""
        print(f"\n{'='*55}")
        print(f"  DASHBOARD COBIT 2019 — CloudCore SaaS | {self.period}")
        print(f"{'='*55}")
        for kpi in self.kpis:
            icon = "✓" if kpi.status() == "OK" else "✗"
            print(f"  {icon} {kpi.name:<35} {kpi.value:>7.2f}{kpi.unit}  [{kpi.status()}]")
        print(f"{'='*55}")
        level, desc = self.maturity_level()
        print(f"  Nivel de Madurez: {level}/5 — {desc}")
        print(f"  Estado Gobernanza: {self.governance_status()}")
        print(f"{'='*55}\n")

    def alerts(self) -> list[KPI]:
        """Retorna KPIs en estado ALERTA."""
        return [k for k in self.kpis if k.status() == "ALERTA"]

    def governance_status(self) -> str:
        """Determina el estado general de gobernanza."""
        n_alerts = len(self.alerts())
        if n_alerts == 0:
            return "CONFORME"
        elif n_alerts <= self.MAX_ALERTS_TOLERATED:
            return "OBSERVACIÓN"
        return "NO CONFORME"

    def maturity_level(self) -> tuple[int, str]:
        """Calcula el nivel de madurez COBIT basado en KPIs en OK."""
        ok_count = sum(1 for k in self.kpis if k.status() == "OK")
        total    = len(self.kpis) or 1
        score    = round((ok_count / total) * 5)
        descriptions = {
            5: "Optimizado",
            4: "Cuantitativamente Gestionado",
            3: "Definido",
            2: "Gestionado",
            1: "Inicial",
            0: "Inexistente",
        }
        return score, descriptions.get(score, "Inicial")

    def committee_decision(self) -> list[str]:
        """Genera decisiones del comité de gobierno TI basadas en KPIs."""
        decisions = []
        for kpi in self.alerts():
            decisions.append(
                f"ACCIÓN REQUERIDA: '{kpi.name}' en ALERTA "
                f"(valor {kpi.value:.2f} vs umbral {kpi.threshold:.2f}). "
                f"Asignar responsable y plazo de corrección."
            )
        if not decisions:
            decisions.append("Sin acciones correctivas pendientes. Mantener controles actuales.")
        return decisions

    def to_dict(self) -> dict:
        level, desc = self.maturity_level()
        return {
            "period":           self.period,
            "kpis":             [k.to_dict() for k in self.kpis],
            "alerts_count":     len(self.alerts()),
            "governance_status": self.governance_status(),
            "maturity_level":   level,
            "maturity_desc":    desc,
            "committee_decisions": self.committee_decision(),
        }
