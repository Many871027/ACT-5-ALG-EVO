# -*- coding: utf-8 -*-
try:
    from .common import (
        BENCHMARK_CAPACITY,
        BENCHMARK_ITEMS,
        OPTIMO_GLOBAL_EXACTO,
        ProjectItem,
    )
    from .knapsack_binary import BinaryKnapsackProblem
    from .knapsack_permutation import PermutationKnapsackProblem
    from .knapsack_random_keys import RandomKeysKnapsackProblem
except (ImportError, ValueError):
    from problems.common import (
        BENCHMARK_CAPACITY,
        BENCHMARK_ITEMS,
        OPTIMO_GLOBAL_EXACTO,
        ProjectItem,
    )
    from problems.knapsack_binary import BinaryKnapsackProblem
    from problems.knapsack_permutation import PermutationKnapsackProblem
    from problems.knapsack_random_keys import RandomKeysKnapsackProblem

__all__ = [
    "ProjectItem",
    "BENCHMARK_ITEMS",
    "BENCHMARK_CAPACITY",
    "OPTIMO_GLOBAL_EXACTO",
    "BinaryKnapsackProblem",
    "RandomKeysKnapsackProblem",
    "PermutationKnapsackProblem",
]
