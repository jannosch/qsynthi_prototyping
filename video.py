import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
from datetime import datetime
import subprocess


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


def create(frames, video_fps, frame_amount, sim_fps, slits, barrier_x, barrier_width, n, save=True):
    # FuncAnimation
    fig, ax = plt.subplots()
    plt.axis('off')  # big performance boost

    data = np.abs(frames[0]) ** 2
    cax = ax.imshow(data, cmap='inferno', norm=matplotlib.colors.PowerNorm(vmin=0, vmax=np.max(np.square(np.abs(frames))), gamma=0.4))
    for b in visual_barrier(n, slits, barrier_x, barrier_width):
        ax.add_patch(b)
    fig.colorbar(cax)  # no performance impact (?)

    def animate(i):
        cax.set_array(np.abs(frames[i * sim_fps // video_fps]) ** 2)

    anim = animation.FuncAnimation(fig, animate, frames=frame_amount * video_fps // sim_fps)
    video_filename = f'output/sim_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.mp4'

    if save:
        anim.save(video_filename, fps=video_fps, dpi=150, bitrate=4000)
        print(f'video saved as {video_filename}')

    return video_filename, anim


def combine(audio_filename, video_filename):
    combined_filename = f'output/combination_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.mp4'

    # Construct the ffmpeg command to combine video and audio
    ffmpeg_command = [
        'ffmpeg',
        '-hide_banner',
        '-i', video_filename,   # Input video file
        '-i', audio_filename,   # Input audio file
        '-c:v', 'copy',         # Copy the video stream
        '-c:a', 'aac',          # Encode the audio to AAC (necessary for some formats)
        '-shortest',            # Finish encoding when the shortest input stream ends
        combined_filename         # Output file
    ]

    # Execute the command
    subprocess.run(ffmpeg_command)
    print(f'combination saved as {combined_filename}')
