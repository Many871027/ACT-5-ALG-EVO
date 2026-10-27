# -*- coding: utf-8 -*-
"""Forma 3 de Codificación: Permutacional / Lista de Prioridad (G3 = Pi_n)."""
from random import Random
from typing import Any

try:
    from ..problem import EvolutionProblem
    from .common import BENCHMARK_CAPACITY, BENCHMARK_ITEMS, ProjectItem
except (ImportError, ValueError):
    from problem import EvolutionProblem
    from problems.common import BENCHMARK_CAPACITY, BENCHMARK_ITEMS, ProjectItem


class PermutationKnapsackProblem(EvolutionProblem):
    """Implementación de selección de proyectos mediante Codificación Permutacional."""

    def __init__(
        self,
        capacity: float = BENCHMARK_CAPACITY,
        items: list[ProjectItem] = BENCHMARK_ITEMS,
    ) -> None:
        self.capacity = capacity
        self.items = items
        self.n = len(items)

    def encoding_name(self) -> str:
        return "Codificación 3: Permutacional / Lista de Prioridad (Pi_n)"

    def random_candidate(self, rng: Random) -> list[int]:
        perm = list(range(self.n))
        rng.shuffle(perm)
        return perm

    def phenotype(self, candidate: list[int]) -> list[int]:
        selection = [0] * self.n
        current_cost = 0.0

        for idx in candidate:
            cost = self.items[idx].cost
            if current_cost + cost <= self.capacity:
                selection[idx] = 1
                current_cost += cost

        return selection

    def fitness(self, candidate: list[int]) -> float:
        pheno = self.phenotype(candidate)
        total_val = sum(g * item.value for g, item in zip(pheno, self.items))
        return float(total_val)

    def crossover(self, first: list[int], second: list[int], rng: Random) -> list[int]:
        if self.n < 2:
            return first.copy()
        idx1, idx2 = sorted(rng.sample(range(self.n), 2))
        segment = first[idx1 : idx2 + 1]
        segment_set = set(segment)

        remaining = [item for item in second if item not in segment_set]
        child = remaining[:idx1] + segment + remaining[idx1:]
        return child

    def mutate(self, candidate: list[int], rate: float, rng: Random) -> list[int]:
        child = candidate.copy()
        effective_rate = rate if rate > 0 else 0.15

        if rng.random() < effective_rate:
            i, j = rng.sample(range(self.n), 2)
            child[i], child[j] = child[j], child[i]
        return child

    def describe(self, candidate: list[int]) -> dict[str, Any]:
        pheno = self.phenotype(candidate)
        cost = sum(g * it.cost for g, it in zip(pheno, self.items))
        val = sum(g * it.value for g, it in zip(pheno, self.items))
        selected_names = [it.name for it, g in zip(self.items, pheno) if g == 1]
        order_names = [self.items[idx].name for idx in candidate]
        return {
            "codificacion": self.encoding_name(),
            "proyectos_seleccionados": selected_names,
            "cantidad_proyectos": len(selected_names),
            "costo_total": cost,
            "capacidad_presupuestal": self.capacity,
            "valor_acumulado": val,
            "es_factible": True,
            "orden_prioridad": order_names[:8] + ["..."],
        }
