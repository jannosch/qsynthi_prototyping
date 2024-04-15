import numpy as np
# import matplotlib.pyplot as plt


def gaussian(x, y, n, offset, width):
    x = (x - n / 2.0) / (n / 2.0) - offset[0]
    y = (y - n / 2.0) / (n / 2.0) - offset[1]
    return np.exp(-(x * x + y * y) / (width * width)) + 0j


def parabola(x, y, n, offset, factor):
    x = (x - n / 2.0) / (n / 2.0) - offset[0]
    y = (y - n / 2.0) / (n / 2.0) - offset[1]
    return factor * (x * x + y * y)


def calculate_next_psi(psi, dt, potential):
    n = psi.shape[0]

    # potential-part
    next_psi = psi * np.exp(1j * dt * potential)

    next_psi = np.fft.fft2(next_psi)

    indices = 2 * np.pi * np.min([np.arange(n), n - np.arange(n)], axis=0)
    k = indices.reshape(-1, 1)
    l = indices.reshape(1, -1)
    theta = (k * k + l * l) * dt
    next_psi *= np.exp(1j * theta)

    next_psi = np.fft.ifft2(next_psi)
    return next_psi


def sim(sim_fps=400, duration=5, sim_speed=0.004, slit_style='double'):
    n = 128

    potential = np.array([[parabola(x, y, n, offset=[0, 0], factor=10000) for x in range(n)] for y in range(n)])

    # barrier
    double_slit = [(-4, -2), (2, 4)]
    single_slit = [(-2, 2)]
    slits = single_slit if slit_style == 'single' else double_slit

    barrier_height = 1e60
    barrier = [barrier_height] * n
    for s in slits:
        barrier[n // 2 + s[0]:n // 2 + s[1]] = [0] * (s[1] - s[0])
    for i in range(n):
        potential[:, n // 2 - 1] += barrier

    # simulation
    frame_amount = duration * sim_fps

    frames = np.empty((frame_amount, n, n), dtype=complex)  # for storing the generated images
    frames[0] = np.array([[gaussian(x, y, n, offset=[-0.6, 0.0], width=0.15) for x in range(n)] for y in range(n)])

    # plt.pcolormesh(pow(np.abs(frames[0]), 2.0/3.0), cmap='inferno', vmin=0, vmax=1)
    # plt.pcolormesh(potential, vmin=0, vmax=20000)
    # plt.colorbar()
    # plt.show()

    for i in range(1, frame_amount):
        frames[i] = calculate_next_psi(frames[i-1], sim_speed / sim_fps, potential)

    return frames
