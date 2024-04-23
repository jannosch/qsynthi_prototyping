import numpy as np
# import matplotlib.pyplot as plt


# TODO: Scale to integral = 1
def gaussian(x, y, n, offset, width, imag=False):
    x = (x - n / 2.0) / (n / 2.0) - offset[0]
    y = (y - n / 2.0) / (n / 2.0) - offset[1]
    value = np.exp(-(x * x + y * y) / (width * width))
    return complex(0, value) if imag else value.astype(complex)


def gaussian_impulse(x, y, n, offset, width, impulse=0.1):
    return np.exp(-1.j * 2 * np.pi * impulse * x) * gaussian(x, y, n, offset, width)


def parabola(x, y, n, offset, factor):
    x = (x - n / 2.0) / (n / 2.0) - offset[0]
    y = (y - n / 2.0) / (n / 2.0) - offset[1]
    return factor * (x * x + y * y)


def calculate_next_psi(psi, dt, potential):
    n = psi.shape[0]

    wall = 0
    next_psi = psi
    next_psi[:wall, :] = 0
    next_psi[-wall:, :] = 0
    next_psi[:, :wall] = 0
    next_psi[:, -wall:] = 0

    # potential-part
    next_psi = psi * np.exp(1j * dt * potential)

    next_psi = np.fft.fft2(next_psi)

    indices = 2 * np.pi * np.min(np.array([np.arange(n), n - np.arange(n)]), axis=0)
    k = indices.reshape(-1, 1)
    l = indices.reshape(1, -1)
    theta = (k * k + l * l) * dt
    next_psi *= np.exp(1j * theta)

    next_psi = np.fft.ifft2(next_psi)

    next_psi[:wall, :] = 0
    next_psi[-wall:, :] = 0
    next_psi[:, :wall] = 0
    next_psi[:, -wall:] = 0

    return next_psi


def sim(n, sim_fps, duration, slits, sim_speed, initial_state=None, potential=None):
    if potential is None:
        potential = np.array([[parabola(x, y, n, offset=[0, 0], factor=10000) for x in range(n)] for y in range(n)])

    # barrier
    barrier_height = 1e60
    barrier = [barrier_height] * n
    for s in slits:
        barrier[n // 2 + s[0]:n // 2 + s[1]] = [0] * (s[1] - s[0])
    for i in range(n):
        potential[:, n // 2 - 1] += np.array(barrier)

    # simulation
    frame_amount = duration * sim_fps

    frames = np.empty((frame_amount, n, n), dtype=complex)  # for storing the generated images
    if initial_state is None:
        frames[0] = np.array([[gaussian(x, y, n, offset=[-0.6, 0.0], width=0.05) for x in range(n)] for y in range(n)])
    else:
        frames[0] = initial_state

    # plt.pcolormesh(pow(np.abs(frames[0]), 2.0/3.0), cmap='inferno', vmin=0, vmax=1)
    # plt.pcolormesh(potential, vmin=0, vmax=20000)
    # plt.colorbar()
    # plt.show()

    for i in range(1, frame_amount):
        frames[i] = calculate_next_psi(frames[i-1], sim_speed / sim_fps, potential)

    return frames

#%%
