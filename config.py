# -*- coding: utf-8 -*-
"""Configuración desacoplada del motor evolutivo.

Parámetros generales de control de la búsqueda evolutiva de 7 etapas.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class EvolutionConfig:
    """Parámetros independientes de la codificación y del problema concreto."""

    population_size: int = 100
    generations: int = 150
    mutation_rate: float = 0.08
    crossover_rate: float = 0.85
    tournament_size: int = 3
    elite_count: int = 2
    seed: Optional[int] = None
    budget: Optional[int] = None

    def __post_init__(self) -> None:
        if self.population_size < 2:
            raise ValueError("population_size debe ser al menos 2.")
        if self.generations < 1:
            raise ValueError("generations debe ser al menos 1.")
        if not 0.0 <= self.mutation_rate <= 1.0 or not 0.0 <= self.crossover_rate <= 1.0:
            raise ValueError("Las probabilidades de cruce y mutación deben estar en [0, 1].")
        if not 2 <= self.tournament_size <= self.population_size:
            raise ValueError("tournament_size debe estar entre 2 y population_size.")
        if not 1 <= self.elite_count < self.population_size:
            raise ValueError("elite_count debe estar entre 1 y population_size - 1.")
        if self.budget is not None and self.budget < self.population_size:
            raise ValueError("El presupuesto de evaluaciones debe cubrir al menos la población inicial.")
