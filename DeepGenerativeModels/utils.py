import numpy as np

def make_fan(
    n_samples=2000,
    n_arms=6,
    noise=0.05,
    random_state=None
):
    rng = np.random.default_rng(random_state)

    samples_per_arm = n_samples // n_arms
    X = []

    for k in range(n_arms):
        # variable radial
        r = rng.uniform(0.0, 1.0, samples_per_arm)

        # ángulo: abanico
        theta = r * 2 * np.pi / n_arms + k * 2 * np.pi / n_arms

        x = r * np.cos(theta)
        y = r * np.sin(theta)

        arm = np.stack([x, y], axis=1)
        arm += noise * rng.standard_normal(arm.shape)

        X.append(arm)

    return np.vstack(X)
