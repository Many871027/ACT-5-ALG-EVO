# -*- coding: utf-8 -*-
"""Motor evolutivo común y desacoplado basado en la metodología de 7 etapas."""
from dataclasses import dataclass
from random import Random
from statistics import mean, pstdev
from time import perf_counter
from typing import Any, Optional

try:
    from .config import EvolutionConfig
    from .problem import EvolutionProblem
except (ImportError, ValueError):
    from config import EvolutionConfig
    from problem import EvolutionProblem


@dataclass
class EvolutionResult:
    """Resultado consolidado de una ejecución evolutiva."""

    best_candidate: Any
    best_fitness: float
    best_phenotype: Any
    generations_completed: int
    evaluations_count: int
    generation_best_found: int
    execution_time: float
    history: list[dict[str, Any]]
    final_diversity: float


class EvolutionEngine:
    """Motor evolutivo agnóstico de la representación del cromosoma."""

    def __init__(self, problem: EvolutionProblem, config: EvolutionConfig) -> None:
        self.problem = problem
        self.config = config
        self.rng = Random(config.seed)
        self.evaluations_count = 0

    def _evaluate_candidate(self, candidate: Any) -> float:
        self.evaluations_count += 1
        return self.problem.fitness(candidate)

    def _tournament(self, population: list[Any], scores: list[float]) -> Any:
        indices = self.rng.sample(range(len(population)), self.config.tournament_size)
        best_index = max(indices, key=lambda idx: scores[idx])
        return population[best_index]

    def _phenotypic_diversity(self, population: list[Any]) -> float:
        if not population:
            return 0.0
        unique_phenotypes = {str(self.problem.phenotype(ind)) for ind in population}
        return len(unique_phenotypes) / len(population)

    # 1. INICIALIZACIÓN (M01-M04)
    def initialize_population(self) -> list[Any]:
        return [
            self.problem.repair(self.problem.random_candidate(self.rng), self.rng)
            for _ in range(self.config.population_size)
        ]

    # 2. EVALUACIÓN (M05-M08)
    def evaluate_population(self, population: list[Any]) -> list[float]:
        return [self._evaluate_candidate(candidate) for candidate in population]

    # 3. SELECCIÓN (M09-M12: Torneo k=tournament_size)
    def select_population(
        self, population: list[Any], scores: list[float], count: Optional[int] = None
    ) -> list[Any]:
        selected_count = count or (self.config.population_size - self.config.elite_count)
        return [self._tournament(population, scores) for _ in range(selected_count)]

    # 4. RECOMBINACIÓN (M13-M16)
    def crossover_population(self, parents: list[Any]) -> list[Any]:
        offspring: list[Any] = []
        for i in range(0, len(parents), 2):
            p1 = parents[i]
            if i + 1 >= len(parents):
                offspring.append(p1)
                continue
            p2 = parents[i + 1]
            if self.rng.random() < self.config.crossover_rate:
                c1 = self.problem.crossover(p1, p2, self.rng)
                c2 = self.problem.crossover(p2, p1, self.rng)
                offspring.extend([c1, c2])
            else:
                offspring.extend([p1, p2])
        return offspring

    # 5. MUTACIÓN (M17-M20)
    def mutate_population(self, offspring: list[Any]) -> list[Any]:
        return [
            self.problem.mutate(child, self.config.mutation_rate, self.rng)
            for child in offspring
        ]

    # 6. REEMPLAZO Y SUPERVIVENCIA (M21-M24: Elitismo estricto M22)
    def replace_population(
        self, population: list[Any], scores: list[float], offspring: list[Any]
    ) -> list[Any]:
        elite_indices = sorted(
            range(len(population)), key=lambda idx: scores[idx], reverse=True
        )
        next_population = [
            population[idx] for idx in elite_indices[: self.config.elite_count]
        ]
        for child in offspring:
            if len(next_population) >= self.config.population_size:
                break
            repaired_child = self.problem.repair(child, self.rng)
            next_population.append(repaired_child)
        return next_population

    # 7. CRITERIO DE PARO Y EJECUCIÓN (M25-M30)
    def run(self) -> EvolutionResult:
        start_time = perf_counter()
        population = self.initialize_population()
        history: list[dict[str, Any]] = []
        best_candidate: Any = None
        best_fitness = float("-inf")
        generation_best_found = 0

        for generation in range(self.config.generations + 1):
            scores = self.evaluate_population(population)
            gen_best_idx = max(range(len(population)), key=lambda idx: scores[idx])
            gen_best_candidate = population[gen_best_idx]
            gen_best_fitness = scores[gen_best_idx]
            mean_fit = mean(scores)
            std_fit = pstdev(scores) if len(scores) > 1 else 0.0
            div = self._phenotypic_diversity(population)

            if gen_best_fitness > best_fitness:
                best_candidate = gen_best_candidate
                best_fitness = gen_best_fitness
                generation_best_found = generation

            history.append({
                "generation": generation,
                "evaluations": self.evaluations_count,
                "best_fitness": gen_best_fitness,
                "mean_fitness": mean_fit,
                "std_fitness": std_fit,
                "diversity": div,
            })

            # Paro por generaciones o presupuesto
            if generation >= self.config.generations:
                break
            if self.config.budget is not None and self.evaluations_count >= self.config.budget:
                break

            parents = self.select_population(population, scores)
            offspring = self.crossover_population(parents)
            offspring = self.mutate_population(offspring)
            population = self.replace_population(population, scores, offspring)

        elapsed = perf_counter() - start_time
        best_pheno = self.problem.phenotype(best_candidate)
        return EvolutionResult(
            best_candidate=best_candidate,
            best_fitness=best_fitness,
            best_phenotype=best_pheno,
            generations_completed=len(history) - 1,
            evaluations_count=self.evaluations_count,
            generation_best_found=generation_best_found,
            execution_time=elapsed,
            history=history,
            final_diversity=history[-1]["diversity"],
        )
