import subprocess
import keyboard  # To detect keypresses
import os
import time
import tkinter as tk
from threading import Timer
import ctypes

FPS = 30  # Frames per second
DURATION = 20  # Duration in seconds for the last portion to save
OUTPUT_DIR = "C:\\LANClips\\OneDrive\\LAN\\"
BUFFER_FILE = "temp_buffer.mp4"

recording_process = None

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def start_ffmpeg_recording():
    """Starts an FFmpeg process to record only the primary screen and save it in segments."""
    global recording_process
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'gdigrab',  # Capture desktop for Windows
        '-framerate', str(FPS),  # Framerate of the screen capture
        '-offset_x', '0',  # Start at the top-left corner (0,0)
        '-offset_y', '0',
        '-video_size', f'{user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}',  # Screen resolution
        '-i', 'desktop',  # Capture desktop
        '-c:v', 'libx264', #libx264
        '-preset', 'ultrafast',  # Reduce CPU usage
        '-pix_fmt', 'yuv420p',
        '-f', 'segment',  # Output segmented files
        '-segment_time', '1',  # Create 1-second segments
        '-force_key_frames', 'expr:gte(t,n_forced*1)',  # Force keyframes every 1 second
        '-reset_timestamps', '1',  # Reset timestamps for each segment
        '-segment_wrap', '40',  # Keep only the last 20 segments
        os.path.join(OUTPUT_DIR, 'temp_buffer_%03d.mp4')  # Output file naming pattern
    ]

    # Start the FFmpeg process in a subprocess
    recording_process = subprocess.Popen(command)


import tkinter as tk
from threading import Timer

def show_notification(message, duration=2):
    """Display a sleek temporary overlay with a message."""
    root = tk.Tk()
    root.overrideredirect(True)  # Remove window decorations
    root.attributes('-topmost', True)  # Keep the window on top
    root.config(bg='black')  # Set background color

    # Get the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Define notification window size
    window_width = 300
    window_height = 80

    # Calculate position for bottom-right corner display
    x_position = screen_width - window_width - 20  # 20 pixels from right edge
    y_position = screen_height - window_height - 20  # 20 pixels from bottom edge

    # Set window geometry
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Create a label with styled message
    label = tk.Label(root, text=message, font=('Helvetica', 14, 'bold'), bg='black', fg='white', padx=20, pady=10)
    label.pack(expand=True)

    # Add fade-out effect
    def close_notification():
        root.after(500, lambda: root.destroy())  # Optional fade-out delay before closing

    Timer(duration, close_notification).start()

    root.mainloop()

def save_clip():
    global recording_process
    uname = os.getlogin()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_filename = os.path.join(OUTPUT_DIR, f"{uname}_{timestr}_clip.mp4")

    # Stop the current recording to ensure the segments are up to date
    recording_process.terminate()
    recording_process.wait()

    # Create a text file listing all the segments (since there are 40 segments)
    segment_list = os.path.join(OUTPUT_DIR, 'segment_list.txt')
    with open(segment_list, 'w') as f:
        for i in range(40):  # Concatenate all 40 segments
            f.write(f"file 'temp_buffer_{i:03d}.mp4'\n")

    # Temporary file to hold the full concatenated result before trimming
    full_temp_file = os.path.join(OUTPUT_DIR, "full_temp_buffer.mp4")

    # Concatenate all segments into a single temporary file
    concat_command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'concat',  # Concatenate mode
        '-safe', '0',  # Allow unsafe file paths
        '-i', segment_list,  # Input segment list
        '-c', 'copy',  # Copy without re-encoding
        full_temp_file  # Temporary output
    ]

    subprocess.call(concat_command)

    # Now trim the concatenated file to only keep the last 20 seconds
    trim_command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-sseof', '-20',  # Start 20 seconds from the end
        '-i', full_temp_file,  # Input the concatenated file
        '-c', 'copy',  # Copy without re-encoding
        output_filename  # Final output file
    ]

    subprocess.call(trim_command)
    print(f"Recording saved as {output_filename}")
    show_notification("Clip saved!", duration=2)

    # Restart the recording process after saving the clip
    start_ffmpeg_recording()

def main():
    """Main function to start screen capture and handle keypress events."""
    print("Press F9 to save the last 20 seconds of video...")

    # Start FFmpeg in a circular buffer mode
    start_ffmpeg_recording()

    try:
        # Main loop to detect key press using the keyboard library
        while True:
            if keyboard.is_pressed('F9'):
                print("F9 pressed: Saving clip...")
                save_clip()
                time.sleep(1)  # Add a short delay to avoid multiple triggers in quick succession

            time.sleep(0.1)  # Small delay to avoid CPU overuse
    finally:
        # Make sure to terminate the recording process when the script ends
        if recording_process:
            recording_process.terminate()

if __name__ == "__main__":
    main()
