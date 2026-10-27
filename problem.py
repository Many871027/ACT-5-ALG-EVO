# -*- coding: utf-8 -*-
"""Contrato abstracto para problemas desacoplados del motor evolutivo.

Permite conectar múltiples formas de codificación cromosómica (binaria,
claves aleatorias, permutacional, etc.) manteniendo un motor unificado.
"""
from abc import ABC, abstractmethod
from random import Random
from typing import Any


class EvolutionProblem(ABC):
    """Contrato abstracto que implementa cada representación o problema enchufable."""

    @abstractmethod
    def encoding_name(self) -> str:
        """Nombre descriptivo de la codificación cromosómica."""

    @abstractmethod
    def random_candidate(self, rng: Random) -> Any:
        """Genera un cromosoma inicial (genotipo) aleatorio."""

    @abstractmethod
    def fitness(self, candidate: Any) -> float:
        """Calcula la función de aptitud (el motor siempre la maximiza)."""

    @abstractmethod
    def crossover(self, first: Any, second: Any, rng: Random) -> Any:
        """Combina la información genética de dos progenitores y devuelve un hijo."""

    @abstractmethod
    def mutate(self, candidate: Any, rate: float, rng: Random) -> Any:
        """Aplica una perturbación estocástica al cromosoma sin alterar el original."""

    def repair(self, candidate: Any, rng: Random) -> Any:
        """Aplica corrección de invariantes o restricciones duras (opcional)."""
        return candidate

    @abstractmethod
    def phenotype(self, candidate: Any) -> Any:
        """Decodifica el genotipo en el fenotipo canónico interpretable."""

    @abstractmethod
    def describe(self, candidate: Any) -> dict[str, Any]:
        """Traduce la solución a un diccionario informativo legible por humanos."""
