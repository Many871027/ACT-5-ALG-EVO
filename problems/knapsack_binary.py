# -*- coding: utf-8 -*-
"""Forma 1 de Codificación: Binaria Directa (G1 = {0, 1}^n)."""
from random import Random
from typing import Any

try:
    from ..problem import EvolutionProblem
    from .common import BENCHMARK_CAPACITY, BENCHMARK_ITEMS, ProjectItem
except (ImportError, ValueError):
    from problem import EvolutionProblem
    from problems.common import BENCHMARK_CAPACITY, BENCHMARK_ITEMS, ProjectItem


class BinaryKnapsackProblem(EvolutionProblem):
    """Implementación de la selección de proyectos mediante Codificación Binaria Directa."""

    def __init__(
        self,
        capacity: float = BENCHMARK_CAPACITY,
        items: list[ProjectItem] = BENCHMARK_ITEMS,
    ) -> None:
        self.capacity = capacity
        self.items = items
        self.n = len(items)

    def encoding_name(self) -> str:
        return "Codificación 1: Binaria Directa ({0, 1}^n)"

    def random_candidate(self, rng: Random) -> list[int]:
        return [1 if rng.random() < 0.4 else 0 for _ in range(self.n)]

    def _totals(self, candidate: list[int]) -> tuple[float, float]:
        cost = sum(gene * item.cost for gene, item in zip(candidate, self.items))
        val = sum(gene * item.value for gene, item in zip(candidate, self.items))
        return cost, val

    def fitness(self, candidate: list[int]) -> float:
        cost, val = self._totals(candidate)
        if cost <= self.capacity:
            return val
        overload = cost - self.capacity
        return max(0.0, val - 15.0 * overload)

    def crossover(self, first: list[int], second: list[int], rng: Random) -> list[int]:
        return [g1 if rng.random() < 0.5 else g2 for g1, g2 in zip(first, second)]

    def mutate(self, candidate: list[int], rate: float, rng: Random) -> list[int]:
        effective_rate = rate if rate > 0 else (1.0 / self.n)
        return [1 - gene if rng.random() < effective_rate else gene for gene in candidate]

    def repair(self, candidate: list[int], rng: Random) -> list[int]:
        child = candidate.copy()
        while self._totals(child)[0] > self.capacity:
            selected_indices = [idx for idx, g in enumerate(child) if g == 1]
            if not selected_indices:
                break
            worst_idx = min(
                selected_indices,
                key=lambda idx: self.items[idx].value / self.items[idx].cost,
            )
            child[worst_idx] = 0
        return child

    def phenotype(self, candidate: list[int]) -> list[int]:
        repaired = self.repair(candidate, Random(0))
        return repaired

    def describe(self, candidate: list[int]) -> dict[str, Any]:
        cost, val = self._totals(candidate)
        selected_names = [it.name for it, g in zip(self.items, candidate) if g == 1]
        is_feasible = cost <= self.capacity
        return {
            "codificacion": self.encoding_name(),
            "proyectos_seleccionados": selected_names,
            "cantidad_proyectos": len(selected_names),
            "costo_total": cost,
            "capacidad_presupuestal": self.capacity,
            "valor_acumulado": val,
            "es_factible": is_feasible,
        }
