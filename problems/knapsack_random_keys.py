# -*- coding: utf-8 -*-
"""Forma 2 de Codificación: Claves Aleatorias Continuas (Random Keys de Bean, G2 = [0, 1]^n)."""
from random import Random
from typing import Any

try:
    from ..problem import EvolutionProblem
    from .common import BENCHMARK_CAPACITY, BENCHMARK_ITEMS, ProjectItem
except (ImportError, ValueError):
    from problem import EvolutionProblem
    from problems.common import BENCHMARK_CAPACITY, BENCHMARK_ITEMS, ProjectItem


class RandomKeysKnapsackProblem(EvolutionProblem):
    """Implementación de selección de proyectos mediante Claves Aleatorias Continuas (Random Keys)."""

    def __init__(
        self,
        capacity: float = BENCHMARK_CAPACITY,
        items: list[ProjectItem] = BENCHMARK_ITEMS,
    ) -> None:
        self.capacity = capacity
        self.items = items
        self.n = len(items)

    def encoding_name(self) -> str:
        return "Codificación 2: Claves Aleatorias Continuas (Random Keys in [0, 1]^n)"

    def random_candidate(self, rng: Random) -> list[float]:
        return [rng.random() for _ in range(self.n)]

    def phenotype(self, candidate: list[float]) -> list[int]:
        sorted_indices = sorted(range(self.n), key=lambda idx: candidate[idx], reverse=True)
        selection = [0] * self.n
        current_cost = 0.0

        for idx in sorted_indices:
            cost = self.items[idx].cost
            if current_cost + cost <= self.capacity:
                selection[idx] = 1
                current_cost += cost

        return selection

    def fitness(self, candidate: list[float]) -> float:
        pheno = self.phenotype(candidate)
        total_val = sum(g * item.value for g, item in zip(pheno, self.items))
        return float(total_val)

    def crossover(self, first: list[float], second: list[float], rng: Random) -> list[float]:
        alpha = 0.5
        child: list[float] = []
        for g1, g2 in zip(first, second):
            val = alpha * g1 + (1.0 - alpha) * g2
            child.append(max(0.0, min(1.0, val)))
        return child

    def mutate(self, candidate: list[float], rate: float, rng: Random) -> list[float]:
        sigma = 0.15
        child: list[float] = []
        effective_rate = rate if rate > 0 else (1.0 / self.n)

        for gene in candidate:
            if rng.random() < effective_rate:
                noise = rng.gauss(0.0, sigma)
                new_val = max(0.0, min(1.0, gene + noise))
                child.append(new_val)
            else:
                child.append(gene)
        return child

    def describe(self, candidate: list[float]) -> dict[str, Any]:
        pheno = self.phenotype(candidate)
        cost = sum(g * it.cost for g, it in zip(pheno, self.items))
        val = sum(g * it.value for g, it in zip(pheno, self.items))
        selected_names = [it.name for it, g in zip(self.items, pheno) if g == 1]
        return {
            "codificacion": self.encoding_name(),
            "proyectos_seleccionados": selected_names,
            "cantidad_proyectos": len(selected_names),
            "costo_total": cost,
            "capacidad_presupuestal": self.capacity,
            "valor_acumulado": val,
            "es_factible": True,
            "claves_prioridad": [round(c, 3) for c in candidate],
        }
