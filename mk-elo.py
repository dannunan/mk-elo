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


def calculate_adjustments(expected_point_share, point_share) -> np.ndarray:
    """Return changes to player ratings based on difference between
    expected and observed `point_share`."""
    return 250 * (point_share - expected_point_share)


if __name__ == "__main__":
    # Test skill rating convergence with some example players
    true_ratings = np.array([1500, 1250, 1100, 800] + [1000] * 8)
    ratings = [np.array([1000] * 12)]

    for gp in range(25):
        # Emulate gp with `length` races
        length = np.random.choice([4, 6, 8, 12])
        placement = (
            np.random.default_rng()
            .normal(loc=true_ratings, scale=RATING_VAR, size=(length, 12))
            .argsort(axis=1, kind="mergesort")
            .argsort(axis=1, kind="mergesort")
        )
        share = POINTS[placement].sum(axis=0) / (TOTAL * length)
        expected_share = estimate_point_share(ratings[-1], 1000)
        adjustment = calculate_adjustments(expected_share, share)
        ratings.append(ratings[-1] + (length * adjustment))

    import matplotlib.pyplot as plt

    ax = plt.subplot()
    ax.plot(np.array(ratings)[:, :4], label=true_ratings[:4])
    ax.set_title("Convergence to true rating")
    ax.legend(loc="upper right")
    ax.set_ylim([0, 2000])
    ax.set_xlabel("GP number")
    ax.set_ylabel("Rating")
    plt.savefig("static/test")
