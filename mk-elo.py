"""Logic for calculating rating changes from scores."""

import numpy as np

RATING_BASE = 1000
RATING_VAR = 250

POINTS = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15])
TOTAL = POINTS.sum()


def estimate_point_share(ratings: np.ndarray, n=1000) -> np.ndarray:
    """Estimate expected proportion of available points for each rating in `ratings`.
    This assumes player performance is normally distributed, and uses a basic monte carlo
    simulation of `n` races to get scores."""

    assert ratings.ndim == 1, "ratings must be a 1 dimensional array"
    n_players = ratings.shape[0]
    assert n_players <= 12, "maximum number of players is 12"

    ratings = np.pad(
        ratings,
        (0, 12 - n_players),
        mode="constant",
        constant_values=RATING_BASE,
    )

    # Double argsort is intended!
    # The first returns vectors of player id in order of position
    # The second returns vectors of positions in order of player
    # TODO: Surely this is not the best way to do this
    placement = (
        np.random.default_rng()
        .normal(loc=ratings, scale=RATING_VAR, size=(n, 12))
        .argsort(axis=1, kind="mergesort")
        .argsort(axis=1, kind="mergesort")
    )

    # Get average score
    return POINTS[placement].mean(axis=0) / TOTAL


if __name__ == "__main__":
    print(TOTAL * estimate_point_share(np.array([2000, 1500, 1000, 500]), 1000))
