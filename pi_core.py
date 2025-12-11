"""
Pure Monte Carlo π estimation helpers (GUI非依存).
"""

from __future__ import annotations

import random


def run_batch(batch_size: int, rng: random.Random | None = None) -> tuple[int, int]:
    """単位正方形に batch_size 回打点し、(円内ヒット数, 総試行数) を返す。"""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    rng = rng or random.Random()

    hits = 0
    for _ in range(batch_size):
        x = rng.uniform(-1.0, 1.0)
        y = rng.uniform(-1.0, 1.0)
        hits += int(x * x + y * y <= 1.0)
    return hits, batch_size


def estimate_pi(num_samples: int, rng: random.Random | None = None) -> float:
    """num_samples 回の打点で π を推定する（簡易版、テスト用）。"""
    if num_samples <= 0:
        raise ValueError("num_samples must be positive")
    rng = rng or random.Random()

    hits = 0
    total = 0
    # 大きな num_samples にも対応できるようバッチに分ける
    while total < num_samples:
        batch = min(10_000, num_samples - total)
        h, n = run_batch(batch, rng)
        hits += h
        total += n
    return 4 * hits / total
