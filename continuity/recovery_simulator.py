"""
CloudCore SaaS — continuity/recovery_simulator.py
ISO 22301:2019: Simulador de Recuperación ante Desastres
"""
import logging
from domain.continuity import ContinuityScenario, DisruptionType

logger = logging.getLogger(__name__)


class RecoverySimulator:
    """
    Simula escenarios de interrupción del negocio y verifica cumplimiento RTO/RPO.
    Basado en ISO 22301:2019 — Sistemas de Gestión de Continuidad del Negocio.
    """

    def __init__(self, rto_minutes: int = None, rto_hours: float = 4.0):
        # Compatible con código base del profesor (rto_minutes) y uso interno (rto_hours)
        if rto_minutes is not None:
            self.rto_hours = rto_minutes / 60
        else:
            self.rto_hours = rto_hours
        self.scenarios: list[ContinuityScenario] = []

    def simulate_recovery(self, actual_recovery_time: float) -> str:
        """
        Evaluación simple compatible con el código base del profesor.
        actual_recovery_time en minutos.
        """
        if actual_recovery_time <= (self.rto_hours * 60):
            return "Recuperación dentro del RTO"
        return "Incumplimiento del RTO"

    def add_scenario(self, scenario: ContinuityScenario):
        """Agrega un escenario de continuidad al simulador."""
        self.scenarios.append(scenario)

    def run_all(self) -> list[dict]:
        """Ejecuta todos los escenarios y retorna resultados."""
        results = []
        for s in self.scenarios:
            status_rto = "✓ CUMPLE" if s.meets_rto() else f"✗ EXCEDE (+{s.rto_gap_h():.1f}h)"
            status_rpo = "✓ CUMPLE" if s.meets_rpo() else "✗ EXCEDE"
            logger.warning(
                f"[CONTINUITY] {s.scenario_id} | {s.disruption_type.value} | "
                f"RTO: {s.actual_rto_h:.2f}h {status_rto} | "
                f"Impacto: USD {s.financial_impact_usd():,.2f}"
            )
            results.append(s.to_dict())
        return results

    def continuity_summary(self) -> dict:
        """Resumen ejecutivo de continuidad del negocio."""
        if not self.scenarios:
            return {}
        rto_compliant = sum(1 for s in self.scenarios if s.meets_rto())
        rpo_compliant = sum(1 for s in self.scenarios if s.meets_rpo())
        total         = len(self.scenarios)
        total_impact  = sum(s.financial_impact_usd() for s in self.scenarios)
        total_risk    = sum(s.residual_risk_usd() for s in self.scenarios)

        return {
            "total_scenarios":      total,
            "rto_compliant":        rto_compliant,
            "rto_compliance_pct":   round(rto_compliant / total * 100, 1),
            "rpo_compliant":        rpo_compliant,
            "rpo_compliance_pct":   round(rpo_compliant / total * 100, 1),
            "total_financial_impact_usd": round(total_impact, 2),
            "total_residual_risk_usd":    round(total_risk, 2),
            "critical_scenarios":   [
                s.scenario_id for s in self.scenarios if not s.meets_rto()
            ],
        }

    @staticmethod
    def default_scenarios(seed: int = 42) -> list[ContinuityScenario]:
        """Retorna los 5 escenarios estándar de CloudCore SaaS."""
        import random
        random.seed(seed)

        scenarios_data = [
            ("ESC-001", DisruptionType.DATABASE_FAILURE,  0.15, 3000,
             random.uniform(2.5, 6.5),  random.uniform(0.1, 0.5)),
            ("ESC-002", DisruptionType.RANSOMWARE,         0.08, 3000,
             random.uniform(8.0, 24.0), random.uniform(1.0, 4.0)),
            ("ESC-003", DisruptionType.CLOUD_OUTAGE,       0.12, random.randint(1500, 3000),
             random.uniform(1.5, 5.0),  random.uniform(0.05, 0.3)),
            ("ESC-004", DisruptionType.NETWORK_LOSS,       0.20, random.randint(500, 2000),
             random.uniform(0.5, 3.0),  0.0),
            ("ESC-005", DisruptionType.DEPLOY_FAILURE,     0.25, random.randint(100, 800),
             random.uniform(0.5, 2.5),  0.0),
        ]
        result = []
        for sid, dtype, prob, clients, rto_real, rpo_real in scenarios_data:
            s = ContinuityScenario(
                scenario_id=sid, disruption_type=dtype,
                probability=prob, rto_objective_h=4.0,
                rpo_objective_h=0.25, clients_affected=clients,
            )
            s.simulate(actual_rto_h=rto_real, actual_rpo_h=rpo_real)
            result.append(s)
        return result
