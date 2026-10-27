# Motor Evolutivo: Comparación de Esquemas de Codificación de Cromosomas en Algoritmos Genéticos

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-Academic-lightgrey.svg)]()

> **Universidad Politécnica Metropolitana de Hidalgo (UPMH)**  
> **Maestría en Inteligencia Artificial y Robótica**  
> **Asignatura:** Algoritmos Evolutivos — Actividad 05  
> **Autores:**  
> - 253220027 — Gutiérrez Salazar, Víctor Manuel  
> - 253220037 — Camacho Ruiz, Diego Armando  
> - 253220033 — Robles Reyes, José Luis  

---

## 1. Descripción del Proyecto

Este repositorio contiene la implementación del motor evolutivo modular diseñado para evaluar y comparar empíricamente el impacto de **tres esquemas de codificación cromosómica** en la resolución del problema de **Optimización de Cartera de Proyectos Tecnológicos** (instancia formal del *0-1 Knapsack Problem*, $n=20$ proyectos, capacidad presupuestal $C=100$).

El óptimo global analítico de referencia ($V^* = 384$ unidades de valor) fue validado mediante **Programación Dinámica**.

---

## 2. Esquemas de Codificación Implementados

| Esquema | Espacio Genotípico ($\mathcal{G}$) | Mapeo Genotipo $\to$ Fenotipo | Tratamiento de Restricción ($C=100$) | Operadores Genéticos |
| :--- | :--- | :--- | :--- | :--- |
| **1. Binaria Directa** | $\mathcal{G}_1 = \{0, 1\}^n$ | Biyectivo directo: $x_i = g_i$ | Penalización cuadrática en función objetivo | Crossover uniforme, mutación bit-flip ($p_m=0.05$) |
| **2. Claves Aleatorias (*Random Keys*)** | $\mathcal{G}_2 = [0, 1]^n$ | Decodificador continuo: ordenamiento relativo $\text{argsort}$ + *First-Fit* | Factibilidad garantizada por construcción decodificadora | Crossover BLX-$\alpha$ ($\alpha=0.3$), mutación gaussiana ($\sigma=0.1$) |
| **3. Permutacional Canónica** | $\mathcal{G}_3 = \Pi_n$ | Orden de prioridad ordinal + decodificación voraz *First-Fit* | Factibilidad estricta asegurada en la decodificación | Order Crossover (OX-1), mutación Swap ($p_m=0.10$) |

---

## 3. Pipeline Evolutivo Canónico de 7 Etapas

El motor implementa las 7 etapas de Goldberg (1989) y Eiben & Smith (2015):
1. **M01 — Inicialización:** Generación estocástica uniforme de la población ($N=60$).
2. **M06 — Evaluación:** Cálculo de aptitud penalizada o fenotípica según la codificación.
3. **M11 — Selección de Padres:** Selección por Torneo Determinista ($k=3$).
4. **M16 — Cruce / Recombinación:** Operadores específicos por espacio genotípico ($p_c=0.85$).
5. **M21 — Mutación:** Exploración perturbativa adaptada ($p_m \in [0.05, 0.10]$).
6. **M25 — Reemplazo:** Mecanismo generacional con elitismo estricto ($\text{elite}=2$).
7. **M30 — Criterio de Parada:** Presupuesto computacional fijo de 100 generaciones ($6{,}000$ evaluaciones).

---

## 4. Resultados del Benchmark Experimental (30 Réplicas Independientes)

Se ejecutaron 30 semillas pseudoaleatorias controladas ($\text{seeds} \in [42, 71]$) para cada codificación:

| Métrica | Codificación Binaria | Claves Aleatorias (*Random Keys*) | Codificación Permutacional |
| :--- | :---: | :---: | :---: |
| **Óptimo Global ($V^* = 384$)** | **384.00** | **384.00** | **384.00** |
| **Tasa de Éxito al Óptimo** | **100.0%** (30/30) | **70.0%** (21/30) | **83.3%** (25/30) |
| **Valor Medio $\pm$ Desv. Est.** | **384.00 $\pm$ 0.00** | **383.37 $\pm$ 1.07** | **383.63 $\pm$ 0.93** |
| **Generación de Convergencia** | $39.53 \pm 18.23$ | $23.13 \pm 18.77$ | **$18.63 \pm 14.86$** |
| **Diversidad Fenotípica Final** | **$56.40\% \pm 8.78\%$** | $7.63\% \pm 4.09\%$ | $5.57\% \pm 3.12\%$ |

### Figuras Comparativas
- **Figura 1:** Curvas de convergencia de aptitud a lo largo de las 100 generaciones.
- **Figura 2:** Evolución de la diversidad fenotípica poblacional.
- **Figura 3:** Distribución estadística (Diagrama de caja y bigotes) de soluciones finales.
- **Figura 4:** Mapeo de dispersión en el espacio de soluciones (Costo presupuestal vs. Valor total).

---

## 5. Estructura del Repositorio

```text
evolutionary-engine/
├── problems/
│   ├── __init__.py
│   ├── common.py                # Definición de la instancia (20 proyectos, C=100, DP solver)
│   ├── knapsack_binary.py       # Codificación 1: Binaria directa
│   ├── knapsack_random_keys.py  # Codificación 2: Claves aleatorias (Bean, 1994)
│   └── knapsack_permutation.py  # Codificación 3: Permutacional canónica
├── config.py                    # Dataclass EvolutionConfig y parámetros
├── problem.py                   # Clase base abstracta EvolutionProblem
├── engine.py                    # Motor evolutivo canónico de 7 etapas
├── benchmark.py                 # Protocolo de 30 réplicas con generación de figuras y JSON
├── ejecutar.py                  # Interfaz de línea de comandos (CLI) interactiva
├── generar_reporte_actividad_05.py # Generador del reporte Word (.docx)
├── resultados_benchmark_codificaciones.json # Métricas completas del benchmark
├── figura_1_convergencia_comparativa.png
├── figura_2_diversidad_fenotipica.png
├── figura_3_distribucion_boxplot.png
├── figura_4_espacio_soluciones.png
└── README.md
```

---

## 6. Instrucciones de Uso

### Requisitos Previos
```bash
pip install numpy matplotlib reportlab python-docx
```

### Ejecución de una Codificación Específica (CLI)
```bash
# Codificación Binaria
python ejecutar.py --codificacion binaria --semilla 42

# Claves Aleatorias
python ejecutar.py --codificacion random_keys --semilla 42

# Permutacional
python ejecutar.py --codificacion permutacion --semilla 42
```

### Ejecución del Benchmark Experimental Completo (30 réplicas)
```bash
python benchmark.py
```
Este comando ejecutará las 90 simulaciones, generará el archivo `resultados_benchmark_codificaciones.json` y exportará las 4 figuras en alta resolución (300 DPI).

---

## 7. Referencias

- Bean, J. C. (1994). Genetic algorithms and random keys for sequencing and optimization. *ORSA Journal on Computing*, 6(2), 154–160.
- Eiben, A. E., & Smith, J. E. (2015). *Introduction to Evolutionary Computing* (2nd ed.). Springer.
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*. Addison-Wesley.
- Martello, S., & Toth, P. (1990). *Knapsack Problems: Algorithms and Computer Implementations*. John Wiley & Sons.
