# -*- coding: utf-8 -*-
"""CLI interactivo para el motor evolutivo multi-codificación.

Permite ejecutar de forma independiente cualquiera de las tres formas de codificación:
  - binaria: Codificación 1 (Binaria Directa)
  - random_keys: Codificación 2 (Claves Aleatorias de Bean)
  - permutacion: Codificación 3 (Permutacional / Lista de Prioridad)
  - todas: Ejecuta las tres en secuencia sobre una misma semilla
  - benchmark: Lanza la batería de 30 réplicas y genera los gráficos comparativos
"""
import argparse
import json
from pathlib import Path
import sys

from config import EvolutionConfig
from engine import EvolutionEngine
from problems import (
    BENCHMARK_CAPACITY,
    OPTIMO_GLOBAL_EXACTO,
    BinaryKnapsackProblem,
    PermutationKnapsackProblem,
    RandomKeysKnapsackProblem,
)

PROBLEMAS = {
    "binaria": BinaryKnapsackProblem,
    "random_keys": RandomKeysKnapsackProblem,
    "permutacion": PermutationKnapsackProblem,
}


def main():
    parser = argparse.ArgumentParser(
        description="Optimizador Evolutivo Multi-Codificación (Actividad 05)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--codificacion",
        choices=["binaria", "random_keys", "permutacion", "todas", "benchmark"],
        default="todas",
        help="Codificación cromosómica a ejecutar (default: todas)",
    )
    parser.add_argument("--semilla", type=int, default=42, help="Semilla pseudoaleatoria (default: 42)")
    parser.add_argument("--poblacion", type=int, default=100, help="Tamaño poblacional (default: 100)")
    parser.add_argument("--generaciones", type=int, default=150, help="Número de generaciones (default: 150)")
    parser.add_argument("--salida-json", type=str, default=None, help="Ruta para exportar el resultado a JSON")
    args = parser.parse_args()

    print("=" * 80)
    print("UNIVERSIDAD POLITÉCNICA METROPOLITANA DE HIDALGO")
    print("MAESTRÍA EN INTELIGENCIA ARTIFICIAL - ALGORITMOS EVOLUTIVOS")
    print("ESTUDIO COMPARATIVO DE TRES FORMAS DE CODIFICACIÓN CROMOSÓMICA")
    print("=" * 80)

    if args.codificacion == "benchmark":
        from benchmark import ejecutar_estudio_comparativo
        ejecutar_estudio_comparativo()
        return

    cfg = EvolutionConfig(
        population_size=args.poblacion,
        generations=args.generaciones,
        crossover_rate=0.85,
        mutation_rate=0.08,
        tournament_size=3,
        elite_count=2,
        seed=args.semilla,
    )

    seleccionadas = (
        ["binaria", "random_keys", "permutacion"]
        if args.codificacion == "todas"
        else [args.codificacion]
    )

    resultados = {}
    for key in seleccionadas:
        prob = PROBLEMAS[key]()
        motor = EvolutionEngine(prob, cfg)
        res = motor.run()
        desc = prob.describe(res.best_candidate)

        brecha = 100.0 * (OPTIMO_GLOBAL_EXACTO - res.best_fitness) / OPTIMO_GLOBAL_EXACTO
        print(f"\n[RESULTADO: {prob.encoding_name()}]")
        print(f"Mejor Fitness alcanzado:      {res.best_fitness:.2f} / {OPTIMO_GLOBAL_EXACTO:.0f} (Óptimo exacto)")
        print(f"Brecha respecto al óptimo:    {brecha:.2f}%")
        print(f"Generación de hallazgo:       Gen {res.generation_best_found} de {res.generations_completed}")
        print(f"Evaluaciones consumidas:      {res.evaluations_count:,}")
        print(f"Diversidad fenotípica final:  {res.final_diversity:.2%}")
        print(f"Tiempo de ejecución:          {res.execution_time:.4f} segundos")
        print(f"Proyectos seleccionados ({desc['cantidad_proyectos']}): {desc['proyectos_seleccionados']}")
        print(f"Costo presupuestal:           {desc['costo_total']:.1f} / {desc['capacidad_presupuestal']:.1f}")

        resultados[key] = {
            "codificacion": prob.encoding_name(),
            "best_fitness": res.best_fitness,
            "brecha_optimo_pct": brecha,
            "generation_best_found": res.generation_best_found,
            "evaluations_count": res.evaluations_count,
            "final_diversity": res.final_diversity,
            "execution_time": res.execution_time,
            "detalle": desc,
        }

    if args.salida_json:
        with open(args.salida_json, "w", encoding="utf-8") as f:
            json.dump(resultados, f, indent=2, ensure_ascii=False)
        print(f"\nResultados guardados en: {args.salida_json}")

    print("\n" + "=" * 80)
    print("PROCESO FINALIZADO EXITOSAMENTE.")
    print("=" * 80)


if __name__ == "__main__":
    main()
