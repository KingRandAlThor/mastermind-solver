"""Tests du solveur Mastermind (10 couleurs, code à 4 positions)."""

import random
import sys
import tempfile
from pathlib import Path

from mastermind_solver import COLORS, MastermindSolver

MAX_ATTEMPTS = 10


def test_score():
    solver = MastermindSolver(Path(tempfile.gettempdir()) / "mm_test.json")
    cases = [
        (("red", "blue", "green", "yellow"), ("red", "blue", "green", "yellow"), (4, 0)),
        (("red", "blue", "green", "yellow"), ("white", "black", "orange", "purple"), (0, 0)),
        (("red", "blue", "green", "yellow"), ("yellow", "green", "blue", "red"), (0, 4)),
        (("red", "blue", "green", "yellow"), ("red", "blue", "yellow", "green"), (2, 2)),
        (("red", "red", "blue", "blue"), ("blue", "blue", "red", "red"), (0, 4)),
        (("red", "red", "red", "red"), ("red", "blue", "blue", "blue"), (1, 0)),
    ]
    for guess, secret, expected in cases:
        assert solver.calculate_score(guess, secret) == expected, (guess, secret)


def solve(secret, checkpoint):
    solver = MastermindSolver(checkpoint)
    for attempt in range(1, MAX_ATTEMPTS + 1):
        guess = solver.choose_next_guess()
        if guess == secret:
            return attempt
        solver.filter_possible_codes(guess, *solver.calculate_score(guess, secret))
    return None


def test_random_codes(count=10, seed=42):
    rng = random.Random(seed)
    checkpoint = Path(tempfile.gettempdir()) / "mm_test.json"
    results = []
    for _ in range(count):
        secret = tuple(rng.choices(COLORS, k=4))
        attempts = solve(secret, checkpoint)
        assert attempts is not None, f"échec sur {secret}"
        results.append(attempts)
        print(f"{' '.join(secret):<35} -> {attempts} essais")
    checkpoint.unlink(missing_ok=True)
    print(f"Moyenne : {sum(results) / len(results):.2f} essais (max {max(results)})")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    test_score()
    print("Calcul du score : OK")
    test_random_codes()
    print("Tous les tests sont OK")
