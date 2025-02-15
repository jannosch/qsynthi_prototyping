import numpy as np
# import matplotlib.pyplot as plt


def gaussian(x, y, n, offset, width, height, imag=False):
    x = (x - n / 2.0) / (n / 2.0) - offset[0]
    y = (y - n / 2.0) / (n / 2.0) - offset[1]
    value = np.exp(-(x * x / (width * width) + y * y / (height * height)))
    return complex(0, value) if imag else value.astype(complex)


def gaussian_x_impulse(x, y, n, offset, width, height, impulse=0.1):
    return np.exp(-1.j * 2 * np.pi * impulse * x) * gaussian(x, y, n, offset, width, height)


def parabola(x, y, n, offset, factor):
    x = (x - n / 2.0) / (n / 2.0) - offset[0]
    y = (y - n / 2.0) / (n / 2.0) - offset[1]
    return factor[0] * x ** factor[2] + factor[1] * y ** factor[2]


def wall(psi, width):
    if width > 0:
        psi[:width, :] = 0
        psi[-width:, :] = 0
        psi[:, :width] = 0
        psi[:, -width:] = 0
    return psi


def normalized(psi):
    return psi / np.sqrt(np.sum(np.square(np.abs(psi))))


def calculate_next_psi(psi, dt, potential, normalize, wall_width):
    n = psi.shape[0]

    # potential-part
    next_psi = psi * np.exp(1j * dt * potential)

    next_psi = np.fft.fft2(next_psi)

    # kinetic part
    indices = 2 * np.pi * np.min(np.array([np.arange(n), n - np.arange(n)]), axis=0)
    k = indices.reshape(-1, 1)
    l = indices.reshape(1, -1)
    theta = (k * k + l * l) * dt
    next_psi *= np.exp(1j * theta)

    next_psi = np.fft.ifft2(next_psi)

    next_psi = wall(next_psi, wall_width)

    if normalize: next_psi = normalized(next_psi)

    return next_psi


def sim(n, sim_fps, duration, slits, barrier_x, barrier_width, sim_speed, initial_state=None, potential=None, normalize=True, wall_width=0):
    if potential is None:
        potential = np.array([[parabola(x, y, n, offset=(0, 0), factor=(10000, 10000, 2)) for x in range(n)] for y in range(n)])

    # barrier
    barrier_height = 1e60
    barrier = [barrier_height] * n
    for s in slits:
        barrier[n // 2 + s[0]:n // 2 + s[1]] = [0] * (s[1] - s[0])
    potential[:, barrier_x:barrier_x + barrier_width] += np.array(barrier)[:, np.newaxis]

    # simulation
    frame_amount = duration * sim_fps

    frames = np.empty((frame_amount, n, n), dtype=complex)  # for storing the generated images
    if initial_state is None:
        frames[0] = np.array([[gaussian(x, y, n, offset=[-0.6, 0.0], width=0.15, height=0.15) for x in range(n)] for y in range(n)])
    else:
        frames[0] = initial_state

    frames[0] = wall(frames[0], wall_width)
    if normalize: frames[0] = normalized(frames[0])

    # plt.pcolormesh(pow(np.abs(frames[0]), 2.0/3.0), cmap='inferno', vmin=0, vmax=1)
    # plt.pcolormesh(potential, vmin=0, vmax=20000)
    # plt.colorbar()
    # plt.show()

    for i in range(1, frame_amount):
        frames[i] = calculate_next_psi(frames[i-1], sim_speed / sim_fps, potential, normalize, wall_width)

    return frames

# %%
