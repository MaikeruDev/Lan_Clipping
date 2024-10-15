import subprocess
import keyboard  
import os
import time
import tkinter as tk
from threading import Timer
import ctypes

FPS = 30  
DURATION = 20  
OUTPUT_DIR = "C:\\LANClips\\OneDrive\\LAN\\"
BUFFER_FILE = "temp_buffer.mp4"

recording_process = None

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def start_ffmpeg_recording():
    global recording_process
    command = [
        'ffmpeg',
        '-y', 
        '-f', 'gdigrab',  
        '-framerate', str(FPS),
        '-offset_x', '0', 
        '-offset_y', '0',
        '-video_size', str(user32.GetSystemMetrics(0)) + 'x' + str(user32.GetSystemMetrics(1)),  
        '-i', 'desktop', 
        '-c:v', 'libx264',
        '-preset', 'ultrafast',  
        '-pix_fmt', 'yuv420p',
        '-f', 'mpegts', 
        '-t', str(DURATION),  
        BUFFER_FILE
    ]

    recording_process = subprocess.Popen(command)

import tkinter as tk
from threading import Timer

def show_notification(message, duration=2):
    """Display a sleek temporary overlay with a message."""
    root = tk.Tk()
    root.overrideredirect(True) 
    root.attributes('-topmost', True) 
    root.config(bg='black')  

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 300
    window_height = 80

    x_position = screen_width - window_width - 20  
    y_position = screen_height - window_height - 20 

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    label = tk.Label(root, text=message, font=('Helvetica', 14, 'bold'), bg='black', fg='white', padx=20, pady=10)
    label.pack(expand=True)

    def close_notification():
        root.after(500, lambda: root.destroy())  

    Timer(duration, close_notification).start()

    root.mainloop()


def save_clip():
    global recording_process
    uname = os.getlogin()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_filename = os.path.join(OUTPUT_DIR, f"{uname}_{timestr}_clip.mp4")

    recording_process.terminate()
    recording_process.wait()

    command = [
        'ffmpeg',
        '-y',  
        '-i', BUFFER_FILE,
        '-c', 'copy',  
        output_filename
    ]
    
    subprocess.call(command)
    print(f"Recording saved as {output_filename}")
    show_notification("Clip saved!", duration=2)

    start_ffmpeg_recording()

def main():
    """Main function to start screen capture and handle keypress events."""
    print("Press F9 to save the last 20 seconds of video...")

    start_ffmpeg_recording()

    try:
        while True:
            if keyboard.is_pressed('F9'):
                print("F9 pressed: Saving clip...")
                save_clip()
                time.sleep(1)  

            time.sleep(0.1)  
    finally: 
        if recording_process:
            recording_process.terminate()

if __name__ == "__main__":
    main()
