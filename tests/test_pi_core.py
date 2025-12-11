import random

import pytest

from pi_core import estimate_pi, run_batch


def test_run_batch_deterministic_seed():
    rng = random.Random(0)
    hits, total = run_batch(10, rng)
    assert total == 10
    assert hits == 8  # 固定シードでの期待値


def test_estimate_pi_reproducible_small_sample():
    rng = random.Random(0)
    pi_est = estimate_pi(1000, rng)
    assert pi_est == pytest.approx(3.072, rel=0, abs=1e-12)


def test_estimate_pi_close_to_math_pi():
    rng = random.Random(1)
    pi_est = estimate_pi(50_000, rng)
    assert pi_est == pytest.approx(3.1415, rel=0.02)  # 2% 以内を許容
