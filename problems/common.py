# -*- coding: utf-8 -*-
"""Instancia Benchmark Oficial para el Problema de Selección de Proyectos.

Problema de la Mochila 0-1 con 20 iniciativas empresariales de TI.
Capacidad presupuestal fija: C = 100 millones de USD / unidades.
Óptimo global teórico comprobado mediante Programación Dinámica: V* = 384.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectItem:
    name: str
    cost: float
    value: float


# Catálogo oficial de 20 iniciativas empresariales
BENCHMARK_ITEMS = [
    ProjectItem("P01_CloudMigration", 12.0, 48.0),
    ProjectItem("P02_CybersecuritySIEM", 15.0, 52.0),
    ProjectItem("P03_DataLakeLakehouse", 20.0, 75.0),
    ProjectItem("P04_ERPUpgrade", 25.0, 85.0),
    ProjectItem("P05_CRMAutomation", 10.0, 38.0),
    ProjectItem("P06_DevSecOpsPipeline", 8.0, 32.0),
    ProjectItem("P07_MobileAppRevamp", 14.0, 50.0),
    ProjectItem("P08_PredictiveAnalytics", 18.0, 68.0),
    ProjectItem("P09_IoTMonitoring", 16.0, 55.0),
    ProjectItem("P10_ZeroTrustAccess", 11.0, 42.0),
    ProjectItem("P11_MicroservicesRefactor", 22.0, 70.0),
    ProjectItem("P12_RoboticProcessAutomation", 9.0, 36.0),
    ProjectItem("P13_DisasterRecoverySite", 17.0, 58.0),
    ProjectItem("P14_CustomerPortal", 13.0, 46.0),
    ProjectItem("P15_EmployeeSelfService", 7.0, 28.0),
    ProjectItem("P16_SupplyChainTracking", 19.0, 62.0),
    ProjectItem("P17_BiometricAuth", 10.0, 35.0),
    ProjectItem("P18_AIHelpdeskAgent", 12.0, 45.0),
    ProjectItem("P19_LegacyDecommission", 6.0, 24.0),
    ProjectItem("P20_ComplianceAuditing", 14.0, 49.0),
]

BENCHMARK_CAPACITY = 100.0
OPTIMO_GLOBAL_EXACTO = 384.0  # Calculado analíticamente vía Programación Dinámica
