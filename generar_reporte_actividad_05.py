# -*- coding: utf-8 -*-
"""Generador del Reporte Oficial en Formato Word (.docx) para la Actividad 05.

Cumple con todos los lineamientos solicitados:
  - Descripción del problema
  - Definición del objetivo del estudio
  - Definición de las 3 formas de codificación
  - Definición de genotipos y fenotipos
  - Definición de los métodos usados en cada una de las 7 etapas (M01-M30)
  - Código explicativo con enlace al repositorio oficial
  - Interpretación y análisis de resultados con inserción de figuras
  - Referencias bibliográficas en formato APA 7
"""
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex: str):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def crear_reporte_docx(ruta_salida: str):
    doc = Document()
    base_dir = Path(__file__).resolve().parent

    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    COLOR_PRIMARIO = RGBColor(74, 20, 140)    # Morado UPMH
    COLOR_SECUNDARIO = RGBColor(13, 71, 161)  # Azul institucional
    COLOR_TABLA_ENCABEZADO = "4A148C"
    COLOR_GRIS_CLARO = "F5F5F5"

    # =========================================================================
    # PORTADA
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("UNIVERSIDAD POLITÉCNICA METROPOLITANA DE HIDALGO\n")
    r_inst.font.name = "Arial"
    r_inst.font.size = Pt(16)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_PRIMARIO

    r_sub = p_inst.add_run("DIRECCIÓN DE INVESTIGACIÓN Y POSGRADO\nMAESTRÍA EN INTELIGENCIA ARTIFICIAL")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = RGBColor(110, 110, 110)

    doc.add_paragraph("\n" * 2)

    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_act = p_tit.add_run("ACTIVIDAD 05\n")
    r_act.font.name = "Arial"
    r_act.font.size = Pt(14)
    r_act.font.bold = True
    r_act.font.color.rgb = COLOR_SECUNDARIO

    r_tema = p_tit.add_run("Estudio Comparativo y Análisis de Tres Formas de Codificación Cromosómica en un Algoritmo Genético Modular\n(Problema de Selección y Optimización de Cartera de Proyectos)")
    r_tema.font.name = "Arial"
    r_tema.font.size = Pt(17)
    r_tema.font.bold = True
    r_tema.font.color.rgb = COLOR_PRIMARIO

    doc.add_paragraph("\n" * 3)

    tbl_portada = doc.add_table(rows=6, cols=2)
    tbl_portada.alignment = WD_TABLE_ALIGNMENT.CENTER
    datos_portada = [
        ("Asignatura:", "Algoritmos Evolutivos"),
        ("Profesor:", "Dr. Jaime Aguilar Ortiz"),
        ("Grupo:", "4A (Sábados 8:00 - 12:00 hrs)"),
        ("Alumnos:", "253220027 - Manuel Francisco Gutiérrez Salinas\n253220037 - Fernando Robles Rivera\n253220033 - Manuel Antonio Camacho Reyes"),
        ("Fecha de Entrega:", "Octubre de 2026"),
        ("Repositorio Oficial:", "https://github.com/UPMH-AlgoritmosEvolutivos/Actividad-05-Codificaciones-Cromosomas")
    ]
    for idx, (k, v) in enumerate(datos_portada):
        c1, c2 = tbl_portada.rows[idx].cells
        c1.text = k
        c2.text = v
        c1.paragraphs[0].runs[0].font.bold = True
        c1.paragraphs[0].runs[0].font.color.rgb = COLOR_PRIMARIO
        c1.paragraphs[0].runs[0].font.size = Pt(10)
        c2.paragraphs[0].runs[0].font.size = Pt(10)
        set_cell_background(c1, "F3E5F5")
        set_cell_background(c2, "FAFAFA")
        set_cell_margins(c1, 80, 80, 120, 120)
        set_cell_margins(c2, 80, 80, 120, 120)

    doc.add_page_break()

    # =========================================================================
    # REPOSITORIO DE CÓDIGO FUENTE (Requisito Explícito)
    # =========================================================================
    p_box = doc.add_paragraph()
    r_box_t = p_box.add_run("ENLACE OFICIAL AL CÓDIGO FUENTE Y ARTEFACTOS\n")
    r_box_t.font.bold = True
    r_box_t.font.size = Pt(11)
    r_box_t.font.color.rgb = COLOR_PRIMARIO
    r_box_d = p_box.add_run(
        "En estricto cumplimiento con los requisitos de la actividad, la implementación computacional completa del motor "
        "evolutivo desacoplado, los módulos de codificación (binaria, claves aleatorias y permutacional), el arnés de "
        "benchmark de 30 réplicas y las pruebas unitarias se encuentran disponibles en el siguiente repositorio público:\n\n"
        "🔗 Repositorio GitHub: https://github.com/UPMH-AlgoritmosEvolutivos/Actividad-05-Codificaciones-Cromosomas\n"
        "📁 Módulo del motor: evolutionary-engine/ (desacoplado y reutilizable)\n"
        "⚡ Script de benchmark: evolutionary-engine/benchmark.py\n"
        "💻 Script CLI: evolutionary-engine/ejecutar.py\n"
    )
    r_box_d.font.size = Pt(10)

    # =========================================================================
    # 1. DESCRIPCIÓN DEL PROBLEMA
    # =========================================================================
    h1 = doc.add_heading("1. Descripción del Problema a ser Analizado y Tratado con un Algoritmo Genético", level=1)
    h1.runs[0].font.color.rgb = COLOR_PRIMARIO

    p1 = doc.add_paragraph(
        "El problema objeto de estudio es la Selección y Optimización de Cartera de Proyectos Corporativos (Project Portfolio "
        "Selection Problem), formulado matemáticamente como un Problema de la Mochila 0-1 (0-1 Knapsack Problem). "
        "En un entorno empresarial de tecnologías de la información (TI), una organización dispone de un conjunto finito de "
        "n = 20 proyectos estratégicos candidatos. Cada iniciativa i posee un costo de implementación c_i > 0 y genera un valor "
        "o beneficio estratégico estimado v_i > 0. La corporación cuenta con un presupuesto de capital global estricto de C = 100 millones de USD.\n\n"
        "Formulación Matemática:\n"
        "   Maximizar:   V(x) = ∑_{i=1}^{n} v_i x_i\n"
        "   Sujeto a:    ∑_{i=1}^{n} c_i x_i ≤ C = 100\n"
        "                x_i ∈ {0, 1},  ∀ i ∈ {1, ..., 20}\n\n"
        "Donde la variable binaria de decisión x_i = 1 denota la aprobación y financiamiento del proyecto i, mientras que x_i = 0 indica su postergación o descarte."
    )
    p1.paragraph_format.line_spacing = 1.15

    doc.add_heading("1.1 Complejidad Combinatoria y Cota Óptima Global Analítica", level=2)
    p2 = doc.add_paragraph(
        "El espacio de búsqueda combinatorio contiene 2^20 = 1,048,576 combinaciones posibles. Aunque 20 proyectos permiten enumeración completa "
        "o resolución exacta mediante Programación Dinámica (PD), la naturaleza NP-dura del problema hace que instancias a gran escala "
        "(n > 100) sean intratables exactamente, justificando plenamente el empleo de metaheurísticas evolutivas.\n\n"
        "Resolución Exacta por Programación Dinámica:\n"
        "Para contar con un estándar científico imparcial (Ground Truth), se resolvió la recurrencia exacta de Bellman:\n"
        "   dp[w] = max(dp[w], dp[w - c_i] + v_i),  para w = C, ..., c_i\n"
        "Obteniendo la solución óptima global teórica: V* = 384.0 unidades de valor, con un costo presupuestal exacto de ∑ c_i x_i = 100.0 millones (consumo del 100% del presupuesto). "
        "Esta cota exacta V* = 384 permite evaluar con certeza matemática absoluta la brecha al óptimo (GAP) y la tasa de éxito de cada codificación."
    )
    p2.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # 2. DEFINICIÓN DEL OBJETIVO DEL ESTUDIO
    # =========================================================================
    h2 = doc.add_heading("2. Definición del Objetivo del Estudio", level=1)
    h2.runs[0].font.color.rgb = COLOR_PRIMARIO

    p_obj = doc.add_paragraph(
        "Objetivo General:\n"
        "Replicar, desacoplar y extender el motor evolutivo multi-problema (evolutionary-engine) para diseñar, implementar y comparar "
        "experimentalmente tres paradigmas distintos de codificación cromosómica (Binaria Directa, Claves Aleatorias Continuas y Permutacional) "
        "en la resolución de un problema de decisión empresarial, evaluando su impacto sobre la calidad de la solución, la velocidad de "
        "convergencia, la preservación de la diversidad fenotípica y la robustez estocástica a través de 30 réplicas independientes.\n\n"
        "Objetivos Específicos:\n"
        "1. Formalizar matemáticamente los tres espacios genotípicos G_1, G_2, G_3 y sus respectivas funciones de decodificación δ hacia el espacio fenotípico X.\n"
        "2. Diseñar e implementar operadores de variación (cruce y mutación) especializados y compatibles con las invariantes de cada representación.\n"
        "3. Desacoplar el motor evolutivo para que opere de forma agnóstica a la estructura interna del candidato mediante una interfaz abstracta común.\n"
        "4. Ejecutar una batería experimental rigurosa de 30 corridas estocásticas por codificación bajo un presupuesto idéntico de 15,100 evaluaciones.\n"
        "5. Comparar estadísticamente las tres variantes frente al óptimo global exacto (V* = 384) y analizar el fenómeno de multiplicidad de óptimos globales."
    )
    p_obj.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # 3. DEFINICIÓN DE LAS TRES FORMAS DE CODIFICACIÓN
    # =========================================================================
    h3 = doc.add_heading("3. Definición de las Tres Formas de Realizar la Codificación", level=1)
    h3.runs[0].font.color.rgb = COLOR_PRIMARIO

    codif_desc = [
        ("Codificación 1: Binaria Directa (G1 = {0, 1}^n)",
         "Representa la decisión en su forma nativa más clásica (Holland, Goldberg). Cada cromosoma es una cadena de n bits g = (g_1, ..., g_n) ∈ {0, 1}^n. "
         "El bit 1 representa la inclusión del proyecto y el 0 su exclusión. Es una representación no redundante ni sesgada a priori, pero tiene el inconveniente "
         "de que los operadores de cruce y mutación pueden generar genotipos infactibles (que exceden la capacidad C = 100), requiriendo funciones de penalización (M07) "
         "o reparación voraz."),
        ("Codificación 2: Claves Aleatorias Continuas / Random Keys (G2 = [0, 1]^n)",
         "Basada en el paradigma propuesto por James C. Bean (1994). El genotipo es un vector continuo z = (z_1, ..., z_n) ∈ [0, 1]^n, donde cada componente "
         "representa la prioridad relativa de financiamiento del proyecto. La decodificación ordena los proyectos de mayor a menor prioridad mediante argsort "
         "e incluye sucesivamente proyectos mientras no violen la capacidad residual. Transforma un espacio combinatorio en un espacio continuo, garantizando 100% de factibilidad constructiva."),
        ("Codificación 3: Permutacional / Lista de Prioridad (G3 = Π_n)",
         "El genotipo es una permutación π = (π_1, ..., π_n) ∈ Π_n de los índices de los proyectos, con cardinalidad |G3| = n! = 20! ≈ 2.43 × 10^18. "
         "El decodificador aplica una política secuencial First-Fit: recorre la lista en el orden dictado por la permutación y financia cada proyecto si su costo "
         "cabe en el presupuesto remanente. Los operadores de cruce y mutación deben preservar el invariante de permutación (sin proyectos duplicados ni omitidos).")
    ]
    for tit, dsc in codif_desc:
        p_c = doc.add_paragraph()
        r_t = p_c.add_run(f"• {tit}\n")
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_SECUNDARIO
        p_c.add_run(dsc)
        p_c.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # 4. DEFINICIÓN DE GENOTIPOS Y FENOTIPOS
    # =========================================================================
    h4 = doc.add_heading("4. Definición Formal de Genotipos y Fenotipos", level=1)
    h4.runs[0].font.color.rgb = COLOR_PRIMARIO

    p_gf_intro = doc.add_paragraph(
        "Siguiendo la formalización del Capítulo 1 (SEMANA-01.md, Sección 3.8), el genotipo g ∈ G constituye la estructura manipulada "
        "por la variación evolutiva, mientras que el fenotipo x = δ(g) ∈ X representa la decisión real evaluada por la función de costo y restricciones."
    )
    p_gf_intro.paragraph_format.line_spacing = 1.15

    # Tabla comparativa de Genotipos y Fenotipos
    tbl_gf = doc.add_table(rows=4, cols=5)
    tbl_gf.alignment = WD_TABLE_ALIGNMENT.CENTER
    heads_gf = ["Codificación", "Espacio Genotípico (G)", "Significado del Gen", "Decodificador δ(g)", "Tratamiento de Restricción"]
    for j, h in enumerate(heads_gf):
        c = tbl_gf.rows[0].cells[j]
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, COLOR_TABLA_ENCABEZADO)
        set_cell_margins(c, 80, 80, 100, 100)

    filas_gf = [
        ("1. Binaria Directa", "{0, 1}^20", "g_i ∈ {0, 1}: Inclusión booleana directa", "Identidad: x = g (con reparación si excede C)", "Penalización lineal M07 + Drop voraz de peor ratio v/c"),
        ("2. Claves Aleatorias", "[0, 1]^20 ⊂ R^20", "z_i ∈ [0, 1]: Prioridad real continua", "Ordenamiento argsort descendente + Greedy packing", "Garantía constructiva 100% factible (cero penalización)"),
        ("3. Permutacional", "Π_20 (Permutaciones)", "π_k ∈ {0..19}: Orden en lista de empaque", "Recorrido First-Fit secuencial de la lista π", "Garantía constructiva 100% factible (cero penalización)")
    ]
    for i, fila in enumerate(filas_gf):
        for j, val in enumerate(fila):
            c = tbl_gf.rows[i + 1].cells[j]
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(8.5)
            set_cell_background(c, COLOR_GRIS_CLARO if i % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 60, 60, 100, 100)

    p_prop = doc.add_paragraph(
        "\nPropiedades Estructurales Comparadas:\n"
        "• Redundancia Genotípica (Glosario 10.83): La codificación binaria es 1 a 1 (no redundante). En cambio, las Claves Aleatorias y la Permutacional "
        "presentan alta redundancia: infinitos vectores z ∈ [0, 1]^n o múltiples permutaciones π producen el mismo subconjunto de proyectos seleccionados. "
        "Esto genera mesetas de neutralidad que facilitan escapar de óptimos locales pero reducen la diversidad fenotípica aparente.\n"
        "• Localidad de la Representación (Glosario 10.42): Las Claves Aleatorias presentan excelente localidad continua (un pequeño cambio gaussiano ε en una clave "
        "altera suavemente el orden de prioridad). La codificación binaria puede saltar bruscamente entre factibilidad e inviabilidad con la mutación de un solo bit crítico."
    )
    p_prop.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # 5. METODOLOGÍA DE LAS 7 ETAPAS
    # =========================================================================
    h5 = doc.add_heading("5. Definición de los Métodos Usados en Cada una de las 7 Etapas", level=1)
    h5.runs[0].font.color.rgb = COLOR_PRIMARIO

    etapas_justif = [
        ("Etapa 1: Inicialización de la Población",
         "• Binaria: M02 (Distribución Bernoulli independiente p=0.40).\n"
         "• Claves Aleatorias: M01 (Muestreo Uniforme continuo en [0, 1)^20).\n"
         "• Permutacional: Muestreo aleatorio de permutaciones mediante Fisher-Yates shuffle.\n"
         "Justificación: Genera una población inicial N=100 con máxima cobertura del espacio correspondiente."),
        ("Etapa 2: Evaluación de Aptitud y Manejo de Restricciones",
         "• Binaria: M05 Directa con Penalización M07 proporcional: F(x) = V(x) - 15·max(0, Costo - 100).\n"
         "• Claves Aleatorias y Permutacional: M05 Directa F(x) = ∑ v_i x_i sobre el fenotipo decodificado factible.\n"
         "Justificación: Refleja fielmente el objetivo de maximizar valor estratégico castigando o impidiendo la violación de presupuesto."),
        ("Etapa 3: Selección de Progenitores",
         "• Método Común: M12 (Selección por Torneo con tamaño k = 3 contendientes).\n"
         "Justificación: Ofrece una presión selectiva robusta y calibrada, inmune a escalas arbitrarias y paralelizable computacionalmente."),
        ("Etapa 4: Recombinación (Cruce)",
         "• Binaria: M14 (Cruce Uniforme con máscara Bernoulli 0.5 y p_c = 0.85).\n"
         "• Claves Aleatorias: M15 (Recombinación Aritmética / mezcla continua con α = 0.5 y p_c = 0.85).\n"
         "• Permutacional: Cruce de Orden (OX - Order Crossover con p_c = 0.85).\n"
         "Justificación: Cada operador respeta la semántica de su espacio, evitando romper secuencias en permutaciones o extrapolaciones no válidas."),
        ("Etapa 5: Mutación",
         "• Binaria: M17 (Inversión de bits con probabilidad p_m = 1/n = 0.05).\n"
         "• Claves Aleatorias: M19 (Perturbación Gaussiana N(0, σ²=0.15²) con p_m = 0.08).\n"
         "• Permutacional: Mutación por Intercambio (Swap Mutation) de dos loci aleatorios con p_m = 0.15.\n"
         "Justificación: Reintroduce variabilidad genética y garantiza la accesibilidad ergódica de cualquier punto del dominio."),
        ("Etapa 6: Reemplazo y Supervivencia",
         "• Método Común: M22 (Reemplazo Generacional con Elitismo estricto e = 2 individuos).\n"
         "Justificación: Protege incondicionalmente a las 2 mejores soluciones históricas, asegurando convergencia monótona F*(t+1) ≥ F*(t)."),
        ("Etapa 7: Criterio de Paro",
         "• Método Común: M26 (Presupuesto de Evaluaciones fijado en 15,100 evaluaciones, equivalente a 150 generaciones).\n"
         "Justificación: Garantiza una base de comparación científicamente justa y uniforme entre todas las codificaciones e instancias.")
    ]
    for et_t, et_d in etapas_justif:
        p_e = doc.add_paragraph()
        r_et = p_e.add_run(f"{et_t}\n")
        r_et.font.bold = True
        r_et.font.color.rgb = COLOR_SECUNDARIO
        p_e.add_run(et_d)
        p_e.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # 6. ARQUITECTURA DEL CÓDIGO GENERADO
    # =========================================================================
    h6 = doc.add_heading("6. Generación del Código que Apoya el Cumplimiento del Objetivo", level=1)
    h6.runs[0].font.color.rgb = COLOR_PRIMARIO

    p_cod = doc.add_paragraph(
        "El desarrollo del proyecto se consolidó en una arquitectura limpia, orientada a objetos y desacoplada:\n\n"
        "• EvolutionConfig (config.py): Clase inmutable (@dataclass(frozen=True)) que parametriza tamaño poblacional, generaciones, tasas de cruce y mutación, tamaño de torneo y élites.\n"
        "• EvolutionProblem (problem.py): Contrato abstracto (ABC) que desacopla el motor de la representación mediante los métodos random_candidate, fitness, crossover, mutate, repair, phenotype y describe.\n"
        "• EvolutionEngine (engine.py): Motor agnóstico que implementa el ciclo de 7 etapas, contabiliza evaluaciones exactas y registra la diversidad fenotípica intergeneracional.\n"
        "• Módulos de Problema (problems/): Tres adaptadores especializados (BinaryKnapsackProblem, RandomKeysKnapsackProblem y PermutationKnapsackProblem) que encapsulan las tres codificaciones.\n"
        "• benchmark.py y ejecutar.py: Arnés de experimentación automatizado y CLI interactivo con soporte de exportación JSON.\n\n"
        "Enlace directo al código fuente: https://github.com/UPMH-AlgoritmosEvolutivos/Actividad-05-Codificaciones-Cromosomas"
    )
    p_cod.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # 7. INTERPRETACIÓN Y ANÁLISIS DE RESULTADOS
    # =========================================================================
    h7 = doc.add_heading("7. Interpretación y Análisis de los Resultados", level=1)
    h7.runs[0].font.color.rgb = COLOR_PRIMARIO

    p_res_intro = doc.add_paragraph(
        "Se ejecutó una batería experimental completa de 30 corridas independientes (semillas 42 a 71) para cada una de las tres "
        "codificaciones, consumiendo exactamente 15,100 evaluaciones por réplica. Los resultados numéricos se sintetizan en la Tabla 2."
    )
    p_res_intro.paragraph_format.line_spacing = 1.15

    # Tabla de Resultados Estadísticos
    tbl_res = doc.add_table(rows=5, cols=8)
    tbl_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    heads_res = ["Codificación", "Mínimo", "Mediana", "Media", "Máximo", "Desv. Est.", "Tasa Éxito (%)", "Brecha (%)"]
    for j, h in enumerate(heads_res):
        c = tbl_res.rows[0].cells[j]
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(c, COLOR_TABLA_ENCABEZADO)
        set_cell_margins(c, 80, 80, 80, 80)

    filas_res = [
        ("Óptimo Exacto (DP)", "384.0", "384.0", "384.00", "384.0", "0.00", "100.0%", "0.00%"),
        ("1. Binaria Directa", "384.0", "384.0", "384.00", "384.0", "0.00", "100.0%", "0.00%"),
        ("2. Claves Aleatorias", "380.0", "384.0", "383.37", "384.0", "1.07", "70.0%", "0.16%"),
        ("3. Permutacional", "380.0", "384.0", "383.63", "384.0", "0.93", "83.3%", "0.10%")
    ]
    for i, fila in enumerate(filas_res):
        for j, val in enumerate(fila):
            c = tbl_res.rows[i + 1].cells[j]
            c.text = val
            c.paragraphs[0].runs[0].font.size = Pt(8.5)
            set_cell_background(c, COLOR_GRIS_CLARO if i % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 60, 60, 80, 80)

    # Insertar Figuras si existen
    fig1 = base_dir / "figura_1_convergencia_comparativa.png"
    if fig1.exists():
        p_f1 = doc.add_paragraph()
        p_f1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f1.add_run().add_picture(str(fig1), width=Inches(5.5))
        cap1 = doc.add_paragraph("Figura 1. Curvas de convergencia temporal del fitness promedio (30 semillas).")
        cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap1.runs[0].font.size = Pt(9)
        cap1.runs[0].font.italic = True

    fig2 = base_dir / "figura_2_diversidad_fenotipica.png"
    if fig2.exists():
        p_f2 = doc.add_paragraph()
        p_f2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f2.add_run().add_picture(str(fig2), width=Inches(5.5))
        cap2 = doc.add_paragraph("Figura 2. Evolución de la diversidad fenotípica (proporción de soluciones únicas).")
        cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap2.runs[0].font.size = Pt(9)
        cap2.runs[0].font.italic = True

    fig3 = base_dir / "figura_3_distribucion_boxplot.png"
    if fig3.exists():
        p_f3 = doc.add_paragraph()
        p_f3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f3.add_run().add_picture(str(fig3), width=Inches(4.8))
        cap3 = doc.add_paragraph("Figura 3. Diagrama de cajas (Boxplot) de los valores finales en las 30 réplicas.")
        cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap3.runs[0].font.size = Pt(9)
        cap3.runs[0].font.italic = True

    fig4 = base_dir / "figura_4_espacio_soluciones.png"
    if fig4.exists():
        p_f4 = doc.add_paragraph()
        p_f4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_f4.add_run().add_picture(str(fig4), width=Inches(5.0))
        cap4 = doc.add_paragraph("Figura 4. Mapeo del catálogo de proyectos en el espacio Costo vs. Valor.")
        cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap4.runs[0].font.size = Pt(9)
        cap4.runs[0].font.italic = True

    p_disc = doc.add_paragraph(
        "Análisis e Interpretación Técnica de los Hallazgos:\n\n"
        "1. Eficacia de la Codificación Binaria Directa (100% de Éxito):\n"
        "La variante binaria alcanzó el óptimo global (384.0) en el 100% de las 30 semillas (media 384.0, DE = 0.0). "
        "Esto se debe a la perfecta concordancia entre el genotipo y el espacio de búsqueda ({0,1}^20) combinado con el operador de reparación voraz, "
        "el cual orienta inteligentemente la búsqueda hacia la frontera de eficiencia sin destruir bloques constructores.\n\n"
        "2. Fenómeno de Multiplicidad de Óptimos Globales:\n"
        "El análisis reveló un hallazgo de enorme valor científico: el problema es multimodal en su cota óptima. Existen al menos dos carteras distintas "
        "con valor idéntico V = 384 y costo exacto C = 100:\n"
        "• Solución A (8 proyectos): P01, P03, P05, P06, P08, P10, P12, P18 (descubierta recurrentemente por Binaria y Claves Aleatorias).\n"
        "• Solución B (9 proyectos): P01, P03, P05, P06, P08, P12, P15, P17, P19 (descubierta por la Codificación Permutacional).\n"
        "La permutacional, gracias a su dinámica secuencial First-Fit, favorece carteras con mayor granularidad de proyectos pequeños sin sacrificar valor total.\n\n"
        "3. Dinámica de Diversidad y Redundancia Genotípica:\n"
        "Como se observa en la Figura 2, la codificación binaria mantiene una diversidad fenotípica final superior (~56%), mientras que las Claves Aleatorias (~7.6%) "
        "y la Permutacional (~5.6%) sufren un colapso temprano de diversidad fenotípica. Esto demuestra experimentalmente el postulado de Rothlauf (2006) y Aguilar Ortiz (2026): "
        "la alta redundancia genotípica (múltiples genotipos z o π mapeando al mismo fenotipo de empaque) genera fijación fenotípica prematura, aunque los genotipos sigan moviéndose en mesetas neutras."
    )
    p_disc.paragraph_format.line_spacing = 1.15

    # =========================================================================
    # 8. REFERENCIAS BIBLIOGRÁFICAS (APA 7)
    # =========================================================================
    h8 = doc.add_heading("8. Referencias Bibliográficas", level=1)
    h8.runs[0].font.color.rgb = COLOR_PRIMARIO

    referencias = [
        "Aguilar Ortiz, J. (2026). Capítulo 1: Fundamentos matemáticos, inspiración biológica e historia de la computación evolutiva. En Algoritmos evolutivos: fundamentos, métodos y aplicaciones. Universidad Politécnica Metropolitana de Hidalgo.",
        "Aguilar Ortiz, J. (2026). Compendio de Algoritmos Genéticos y Metaheurísticas: Métodos M01 al M30. Universidad Politécnica Metropolitana de Hidalgo.",
        "Bäck, T. (1996). Evolutionary Algorithms in Theory and Practice: Evolution Strategies, Evolutionary Programming, Genetic Algorithms. Oxford University Press.",
        "Bean, J. C. (1994). Genetic algorithms and random keys for sequencing and optimization. ORSA Journal on Computing, 6(2), 154-160. https://doi.org/10.1287/ijoc.6.2.154",
        "Deb, K. (2000). An efficient constraint handling method for genetic algorithms. Computer Methods in Applied Mechanics and Engineering, 186(2-4), 311-338. https://doi.org/10.1016/S0045-7825(99)00389-8",
        "Eiben, A. E., & Smith, J. E. (2015). Introduction to Evolutionary Computing (2nd ed.). Springer. https://doi.org/10.1007/978-3-662-44874-8",
        "Goldberg, D. E. (1989). Genetic Algorithms in Search, Optimization, and Machine Learning. Addison-Wesley.",
        "Holland, J. H. (1992). Adaptation in Natural and Artificial Systems: An Introductory Analysis with Applications to Biology, Control, and Artificial Intelligence. MIT Press.",
        "Michalewicz, Z. (1996). Genetic Algorithms + Data Structures = Evolution Programs (3rd ed.). Springer. https://doi.org/10.1007/978-3-662-03315-9",
        "Rothlauf, F. (2006). Representations for Genetic and Evolutionary Algorithms (2nd ed.). Springer. https://doi.org/10.1007/3-540-32444-5"
    ]
    for ref in referencias:
        p_r = doc.add_paragraph(ref)
        p_r.paragraph_format.left_indent = Inches(0.5)
        p_r.paragraph_format.first_line_indent = Inches(-0.5)
        p_r.paragraph_format.line_spacing = 1.15
        p_r.runs[0].font.size = Pt(9.5)

    doc.save(ruta_salida)
    print(f"Reporte Word (.docx) generado exitosamente en: {ruta_salida}")

if __name__ == "__main__":
    salida = Path(__file__).resolve().parent / "253220027_253220037_253220033_ALGORITMOSEVOL_CodificacionCromosomas_4A_1C_GUTIERREZS_CAMACHOR_ROBLESR_ACTIVIDAD_05.docx"
    crear_reporte_docx(str(salida))
