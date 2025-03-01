import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from scipy.ndimage import map_coordinates
import time
from datetime import datetime
import subprocess
from pya import *


def normalize_psi(psi):
    return psi / np.sqrt(np.sum(np.square(np.abs(psi))))

def parabolic(frame_size=128, center=dict(x=64, y=64), factor=dict(x=4, y=4), normalize=False):
    x = np.arange(frame_size)[np.newaxis, :]
    y = np.arange(frame_size)[:, np.newaxis]
    frame = (((x - center['x']) * factor['x']) ** 2 + ((y - center['y']) * factor['y']) ** 2).astype(complex)
    if normalize: frame = normalize_psi(frame)
    return frame

def gaussian(frame_size=128, center=dict(x=28, y=64), stretch=dict(x=8, y=8), normalize=False):
    x = np.arange(frame_size)[np.newaxis, :]
    y = np.arange(frame_size)[:, np.newaxis]
    frame = np.exp(-(((x - center['x']) / stretch['x']) ** 2 + ((y - center['y']) / stretch['y']) ** 2)).astype(complex)
    if normalize: frame = normalize_psi(frame)
    return frame

def probability_density(frame):
    return np.square(np.abs(frame))

def border(psi, width):
    if width > 0:
        psi[:width, :] = 0
        psi[-width:, :] = 0
        psi[:, :width] = 0
        psi[:, -width:] = 0
    return psi

def clean_filename(string: str):
    string = string.lower().replace("-", "_").replace(":", "_").replace(".", "_").replace(" ", "_")
    while("__" in string):
        string = string.replace("__", "_")
    return string


class Barrier():
    def __init__(self, x=64, width=1, slits=[], value=1e60):
        self.x = x
        self.width = width
        self.slits = slits
        self.value = value
        
    def to_potential(self, frame_size):
        potential = np.zeros((frame_size, frame_size))
                
        barrier = np.ones(frame_size) * self.value
        for slit in self.slits:
            barrier[slit[0]:slit[1]+1] = 0
            
        potential[:, self.x:self.x + self.width] += barrier[:, np.newaxis]
        return potential
    
    def get_patches(self, frame_size, color='#ffffff'):
        start = 0
        rects = []
        for slit in self.slits:
            end = slit[0]
            rect = patches.Rectangle((self.x - 0.5, start - 0.5), self.width, end - start, linewidth=0, facecolor=color)
            start = slit[1] + 1
            rects.append(rect)
        rects.append(patches.Rectangle((self.x - 0.5, start - 0.5), self.width, frame_size - start, linewidth=0, facecolor=color))
        return rects

        
    

class Simulation():
    def __init__(self, title, fps, speed, initial_state, potential, barrier: Barrier = None, border_width=4, video_gamma=0.5):
        self.title = title
        self.fps = fps
        self.speed = speed
        
        assert(initial_state.shape == potential.shape and initial_state.shape[0] == initial_state.shape[1])
        self.frame_size = initial_state.shape[0]
        self.frames = initial_state[np.newaxis, :, :]
        self.potential = potential
        if barrier:
            self.potential += barrier.to_potential(self.frame_size)
        self.barrier = barrier
        
        self.border_width=4
        
        self.video_gamma = video_gamma
        self.video_filename = None
    
    def num_frames(self):
        return self.frames.shape[0]
    
    def duration_seconds(self):
        return self.num_frames() / self.fps
    
    def get_next_step(self, psi, dt, normalize=True):
        # potential-part
        next_psi = psi * np.exp(1j * dt * self.potential)

        # convert to impulse space
        next_psi = np.fft.fft2(next_psi)

        # kinetic part
        indices = 2 * np.pi * np.min(np.array([np.arange(self.frame_size), self.frame_size - np.arange(self.frame_size)]), axis=0)
        k = indices.reshape(-1, 1)
        l = indices.reshape(1, -1)
        theta = (k * k + l * l) * dt
        next_psi *= np.exp(1j * theta)

        next_psi = np.fft.ifft2(next_psi)

        if self.border_width > 0: next_psi = border(next_psi, self.border_width)
        if normalize: next_psi = normalize_psi(next_psi)
        return next_psi
    
    def simulate_steps(self, num_steps, normalize=True):
        if self.border_width > 0: self.frames[-1] = border(self.frames[-1], self.border_width)
        if normalize: self.frames[-1] = normalize_psi(self.frames[-1])
        
        # Allocate memory
        self.frames = np.append(self.frames, np.empty((num_steps, self.frame_size, self.frame_size), dtype=complex), axis=0)

        for i in range(0, num_steps):
            self.frames[i-num_steps] = self.get_next_step(self.frames[i-num_steps-1], self.speed/self.fps, normalize)
            
        # Remove refrerence to existing video as simulation changed 
        self.video_filename = None
        
    def interpolated(self, indices):
        """
        indices is a floating point numpy array of shape (3, number of retrieved points). Frames is indexed by [timestamp, y, x]
        Returns the values at these indices by using tri-cubic interpolation.
        """
        return map_coordinates(self.frames, np.array(indices), order=3, mode="nearest")
        
    def simulate(self, seconds, normalize=True):
        return self.simulate_steps(num_steps=self.fps * seconds, normalize=normalize)
    
    def render_video(self, video_fps=20, complex_to_real_fn=probability_density, show_axis=True, additional_patches=None):
        fig, ax = plt.subplots()
        if not show_axis: plt.axis('off') # big performance boost

        data = complex_to_real_fn(self.frames[0])
        cax = ax.imshow(data, cmap='inferno', norm=matplotlib.colors.PowerNorm(vmin=0, vmax=np.max(complex_to_real_fn(self.frames)), gamma=self.video_gamma))
        if self.barrier:
            for p in self.barrier.get_patches(self.frame_size):
                ax.add_patch(p)
        if additional_patches:
            for p in additional_patches:
                ax.add_patch(p)
        fig.colorbar(cax) # no performance boost
        if self.title:
            ax.set_title(self.title)

        def animate(i):
            cax.set_array(complex_to_real_fn(self.frames[int(i * self.fps / video_fps)]))

        anim = animation.FuncAnimation(fig, animate, frames=int(self.num_frames() / self.fps * video_fps))
        
        video_filename = f'output/{clean_filename(self.title)}_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.mp4'
        if not additional_patches:
            self.video_filename = video_filename
        anim.save(video_filename, fps=video_fps, dpi=150, bitrate=4000)
        print(f'Video saved as {video_filename}')
        plt.close()
        return video_filename
        
    def video_with_sonification(self, asig, sonification_title="sonification", additional_patches=None, normalize_audio=True):
        if additional_patches:
            video_filename = self.render_video(additional_patches=additional_patches)
        elif not self.video_filename:
            video_filename = self.render_video()
        else:
            video_filename = self.video_filename
            
        # Save asig as audio file
        audio_filename = (f'output/{clean_filename(self.title)}_{clean_filename(sonification_title)}_{datetime.now().strftime("%Y_%m_%d-%H_%M_%S")}.wav')
        if normalize_audio:
            asig = asig.norm()
        asig = asig.fade_in(0.05).fade_out(0.05)
        asig.save_wavfile(audio_filename)
        print(f'Sonification saved as {audio_filename}')
        
        combined_filename = audio_filename.replace('.wav', '.mp4')

        # Construct the ffmpeg command to combine video and audio
        ffmpeg_command = [
            'ffmpeg',
            '-loglevel', 'error',
            '-hide_banner',
            '-i', video_filename,       # Input video file
            '-i', audio_filename,       # Input audio file
            '-c:v', 'copy',             # Copy the video stream
            '-c:a', 'flac',             # If 'flac' doesn't work, try 'aac'
            '-shortest',                # Finish encoding when the shortest input stream ends
            combined_filename           # Output file
        ]

        # Execute the command
        subprocess.run(ffmpeg_command)
        time.sleep(0.2)
        print(f'Video with Sonification saved as {combined_filename}')
        return combined_filename 
