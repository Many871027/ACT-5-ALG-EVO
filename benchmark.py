# -*- coding: utf-8 -*-
"""Arnés Experimental y Benchmark Comparativo de Tres Formas de Codificación.

Ejecuta 30 réplicas estocásticas independientes (semillas 42 a 71) para:
  1. Codificación Binaria Directa
  2. Codificación por Claves Aleatorias (Random Keys)
  3. Codificación Permutacional (Lista de Prioridad)

Calcula métricas estadísticas descriptivas y genera figuras de alta resolución (300 DPI).
"""
import json
from pathlib import Path
from statistics import mean, median, pstdev, stdev
from time import perf_counter
import matplotlib.pyplot as plt
import numpy as np

from config import EvolutionConfig
from engine import EvolutionEngine
from problems import (
    BENCHMARK_CAPACITY,
    BENCHMARK_ITEMS,
    OPTIMO_GLOBAL_EXACTO,
    BinaryKnapsackProblem,
    PermutationKnapsackProblem,
    RandomKeysKnapsackProblem,
)

ENLACE_CODIGO = "https://github.com/UPMH-AlgoritmosEvolutivos/Actividad-05-Codificaciones-Cromosomas"


def ejecutar_estudio_comparativo(
    semillas: range = range(42, 72),
    config_base: EvolutionConfig = EvolutionConfig(population_size=100, generations=150, crossover_rate=0.85, mutation_rate=0.08, elite_count=2, tournament_size=3),
    directorio_salida: Path = Path(__file__).resolve().parent,
) -> dict:
    """Ejecuta las 30 corridas para cada codificación y compila estadísticas."""
    directorio_salida.mkdir(parents=True, exist_ok=True)

    codificaciones = [
        ("Binaria Directa", BinaryKnapsackProblem),
        ("Claves Aleatorias (Random Keys)", RandomKeysKnapsackProblem),
        ("Permutacional (Lista Prioridad)", PermutationKnapsackProblem),
    ]

    resultados_totales = {}
    trayectorias_convergencia = {}
    trayectorias_diversidad = {}

    print("=" * 80)
    print("INICIANDO BENCHMARK COMPARATIVO: TRES FORMAS DE CODIFICACIÓN CROMOSÓMICA")
    print(f"Instancia: Cartera de 20 Proyectos | Presupuesto: {BENCHMARK_CAPACITY} | Óptimo Global Exacto: {OPTIMO_GLOBAL_EXACTO}")
    print(f"Batería experimental: {len(semillas)} semillas ({semillas.start} a {semillas.stop - 1})")
    print("=" * 80)

    for nombre, clase_prob in codificaciones:
        print(f"\n>>> Evaluando: {nombre}...")
        t_inicio_cod = perf_counter()
        fits_finales = []
        tiempos = []
        gen_hallazgos = []
        diversidades_finales = []
        curvas_mejor = []
        curvas_media = []
        curvas_div = []
        soluciones_detalle = []

        for s in semillas:
            cfg = EvolutionConfig(
                population_size=config_base.population_size,
                generations=config_base.generations,
                crossover_rate=config_base.crossover_rate,
                mutation_rate=config_base.mutation_rate,
                tournament_size=config_base.tournament_size,
                elite_count=config_base.elite_count,
                seed=s,
            )
            prob = clase_prob()
            motor = EvolutionEngine(prob, cfg)
            res = motor.run()

            fits_finales.append(res.best_fitness)
            tiempos.append(res.execution_time)
            gen_hallazgos.append(res.generation_best_found)
            diversidades_finales.append(res.final_diversity)

            # Historial de aptitud y diversidad
            curvas_mejor.append([h["best_fitness"] for h in res.history])
            curvas_media.append([h["mean_fitness"] for h in res.history])
            curvas_div.append([h["diversity"] for h in res.history])
            soluciones_detalle.append(prob.describe(res.best_candidate))

        arr_f = np.array(fits_finales)
        exitos = int(np.sum(arr_f >= OPTIMO_GLOBAL_EXACTO))
        tasa_exito = 100.0 * exitos / len(semillas)
        brecha_media = 100.0 * (OPTIMO_GLOBAL_EXACTO - float(arr_f.mean())) / OPTIMO_GLOBAL_EXACTO

        stats = {
            "nombre": nombre,
            "minimo": float(arr_f.min()),
            "mediana": float(np.median(arr_f)),
            "media": float(arr_f.mean()),
            "maximo": float(arr_f.max()),
            "desv_est": float(arr_f.std(ddof=1)),
            "tasa_exito_pct": tasa_exito,
            "brecha_media_optimo_pct": brecha_media,
            "gen_hallazgo_media": float(mean(gen_hallazgos)),
            "diversidad_final_media": float(mean(diversidades_finales)),
            "tiempo_medio_segundos": float(mean(tiempos)),
            "valores_corridas": fits_finales,
        }
        resultados_totales[nombre] = stats

        # Promedios de trayectoria para gráficos
        trayectorias_convergencia[nombre] = {
            "mejor_promedio": np.mean(curvas_mejor, axis=0).tolist(),
            "media_promedio": np.mean(curvas_media, axis=0).tolist(),
        }
        trayectorias_diversidad[nombre] = np.mean(curvas_div, axis=0).tolist()

        t_elapsed = perf_counter() - t_inicio_cod
        print(f"Completado en {t_elapsed:.2f} s | Mediana: {stats['mediana']:.1f} | Media: {stats['media']:.2f} | Éxito: {stats['tasa_exito_pct']:.1f}%")

    # =========================================================================
    # GENERACIÓN DE GRÁFICOS (300 DPI)
    # =========================================================================
    print("\nGenerando figuras analíticas para el reporte...")
    colores = {
        "Binaria Directa": "#1976D2",               # Azul
        "Claves Aleatorias (Random Keys)": "#388E3C",# Verde
        "Permutacional (Lista Prioridad)": "#E64A19", # Naranja oscuro
    }

    generaciones = list(range(config_base.generations + 1))

    # FIGURA 1: Convergencia Comparativa (Mejor Aptitud Promedio a lo largo de 30 semillas)
    plt.figure(figsize=(9, 5.5), dpi=300)
    for nombre, tray in trayectorias_convergencia.items():
        plt.plot(generaciones, tray["mejor_promedio"], label=f"{nombre} (Mejor)", color=colores[nombre], linewidth=2.0)
        plt.plot(generaciones, tray["media_promedio"], linestyle="--", alpha=0.5, color=colores[nombre])
    plt.axhline(OPTIMO_GLOBAL_EXACTO, color="#212121", linestyle=":", linewidth=1.5, label=f"Óptimo Teórico Exacto ({int(OPTIMO_GLOBAL_EXACTO)})")
    plt.title("Evolución del Fitness Promedio por Generación (30 Semillas)", fontsize=11, fontweight="bold")
    plt.xlabel("Generación", fontsize=10, fontweight="bold")
    plt.ylabel("Valor Acumulado de Cartera", fontsize=10, fontweight="bold")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower right", frameon=True)
    plt.tight_layout()
    ruta_fig1 = directorio_salida / "figura_1_convergencia_comparativa.png"
    plt.savefig(ruta_fig1)
    plt.close()

    # FIGURA 2: Diversidad Fenotípica por Generación
    plt.figure(figsize=(9, 5.0), dpi=300)
    for nombre, tray_div in trayectorias_diversidad.items():
        plt.plot(generaciones, tray_div, label=nombre, color=colores[nombre], linewidth=2.0)
    plt.title("Evolución de la Diversidad Fenotípica (Proporción de Soluciones Únicas)", fontsize=11, fontweight="bold")
    plt.xlabel("Generación", fontsize=10, fontweight="bold")
    plt.ylabel("Diversidad Fenotípica (U / N)", fontsize=10, fontweight="bold")
    plt.ylim(-0.02, 1.02)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper right", frameon=True)
    plt.tight_layout()
    ruta_fig2 = directorio_salida / "figura_2_diversidad_fenotipica.png"
    plt.savefig(ruta_fig2)
    plt.close()

    # FIGURA 3: Boxplot Comparativo de las 30 Semillas
    plt.figure(figsize=(8, 5.0), dpi=300)
    nombres_lista = list(resultados_totales.keys())
    datos_cajas = [resultados_totales[nom]["valores_corridas"] for nom in nombres_lista]
    bp = plt.boxplot(datos_cajas, tick_labels=["Binaria Directa", "Claves Aleatorias", "Permutacional"], patch_artist=True, widths=0.45)
    palette = ["#BBDEFB", "#C8E6C9", "#FFCCBC"]
    for patch, col in zip(bp["boxes"], palette):
        patch.set_facecolor(col)
    plt.axhline(OPTIMO_GLOBAL_EXACTO, color="#D32F2F", linestyle=":", linewidth=1.5, label=f"Óptimo Global ({int(OPTIMO_GLOBAL_EXACTO)})")
    plt.title("Distribución de Aptitud Final tras 150 Generaciones (30 Semillas)", fontsize=11, fontweight="bold")
    plt.ylabel("Valor de la Cartera de Proyectos", fontsize=10, fontweight="bold")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="lower right")
    plt.tight_layout()
    ruta_fig3 = directorio_salida / "figura_3_distribucion_boxplot.png"
    plt.savefig(ruta_fig3)
    plt.close()

    # FIGURA 4: Mapeo Espacio de Soluciones (Costo vs Valor de los Proyectos)
    plt.figure(figsize=(8, 5.2), dpi=300)
    costs = [it.cost for it in BENCHMARK_ITEMS]
    values = [it.value for it in BENCHMARK_ITEMS]
    ratios = [v / c for c, v in zip(costs, values)]
    scatter = plt.scatter(costs, values, c=ratios, cmap="viridis", s=140, edgecolor="black", linewidth=1.0, zorder=3)
    cbar = plt.colorbar(scatter)
    cbar.set_label("Eficiencia (Valor / Costo)", fontsize=9, fontweight="bold")
    for it in BENCHMARK_ITEMS:
        plt.annotate(it.name.split("_")[0], (it.cost, it.value), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)
    plt.axvline(BENCHMARK_CAPACITY, color="red", linestyle="--", alpha=0.7, label=f"Capacidad Total ({int(BENCHMARK_CAPACITY)})")
    plt.title("Catálogo de Proyectos: Espacio Costo vs. Valor", fontsize=11, fontweight="bold")
    plt.xlabel("Costo del Proyecto (Millones de USD)", fontsize=10, fontweight="bold")
    plt.ylabel("Valor del Proyecto (Aporte Estratégico)", fontsize=10, fontweight="bold")
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.legend(loc="upper left")
    plt.tight_layout()
    ruta_fig4 = directorio_salida / "figura_4_espacio_soluciones.png"
    plt.savefig(ruta_fig4)
    plt.close()

    # Guardar resumen JSON
    archivo_json = directorio_salida / "resultados_benchmark_codificaciones.json"
    with open(archivo_json, "w", encoding="utf-8") as f:
        json.dump(resultados_totales, f, indent=2, ensure_ascii=False)

    print("\nBenchmark completado exitosamente.")
    print(f"Resumen exportado a: {archivo_json}")
    return resultados_totales


if __name__ == "__main__":
    ejecutar_estudio_comparativo()
