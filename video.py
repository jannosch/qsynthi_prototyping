import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from datetime import datetime
import subprocess
from pya import *


# create visual barrier for plot
def visual_barrier(n, barrier_gaps, barrier_x, barrier_width):
    start = 0
    rects = []
    for g in barrier_gaps:
        end = n//2 + g[0]
        rect = patches.Rectangle((barrier_x - 0.5, start - 0.5), barrier_width, end - start, linewidth=0, facecolor='#60b0ff')
        start = n//2 + g[1]
        rects.append(rect)
    rects.append(patches.Rectangle((barrier_x - 0.5, start - 0.5), barrier_width, n - start, linewidth=0, facecolor='#60b0ff'))
    return rects


def create(frames, video_fps, video_speed, frame_amount, sim_fps, slits, barrier_x, barrier_width, n, complex_to_real_fn=lambda z: np.square(np.abs(z)), show_axis=False, save=True, title=None, gamma=0.5):
    # FuncAnimation
    fig, ax = plt.subplots()
    if not show_axis: plt.axis('off')  # big performance boost

    data = np.abs(frames[0]) ** 2
    cax = ax.imshow(data, cmap='inferno', norm=matplotlib.colors.PowerNorm(vmin=0, vmax=np.max(complex_to_real_fn(frames)), gamma=gamma))
    for b in visual_barrier(n, slits, barrier_x, barrier_width):
        ax.add_patch(b)
    fig.colorbar(cax)  # no performance impact (?)
    if title:
        ax.set_title(title)

    def animate(i):
        cax.set_array(complex_to_real_fn(frames[int(i * sim_fps / video_fps * video_speed)]))

    anim = animation.FuncAnimation(fig, animate, frames=int(frame_amount * video_fps / sim_fps / video_speed))
    video_filename = f'output/sim_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.mp4'

    if save:
        anim.save(video_filename, fps=video_fps, dpi=150, bitrate=4000)
        print(f'Video saved as {video_filename}')

    plt.close()
    return video_filename, anim


def combine(audio_filename, video_filename, result_filename="combination"):
    combined_filename = f'output/{result_filename}_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.mp4'

    # Construct the ffmpeg command to combine video and audio
    ffmpeg_command = [
        'ffmpeg',
        '-loglevel', 'error',
        '-hide_banner',
        '-i', video_filename,   # Input video file
        '-i', audio_filename,   # Input audio file
        '-c:v', 'copy',         # Copy the video stream
        '-c:a', 'flac',         # If FLAC doesn't work, try 'aac'
        '-shortest',            # Finish encoding when the shortest input stream ends
        combined_filename         # Output file
    ]

    # Execute the command
    subprocess.run(ffmpeg_command)
    time.sleep(0.1)
    print(f'Video with Audio saved as {combined_filename}')
    return combined_filename


def combine_asig(asig, video_filename, result_filename="combination", normalize_audio=True):
    audio_filename = (f'output/sonification_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.wav')
    if normalize_audio:
        asig = asig.norm()
    asig = asig.fade_in(0.05).fade_out(0.05)
    asig.save_wavfile(audio_filename)

    return combine(audio_filename, video_filename, result_filename)
