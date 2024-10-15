import subprocess
import keyboard  # To detect keypresses
import os
import time
import tkinter as tk
from threading import Timer
import ctypes
import glob

FPS = 30  # Frames per second
SEGMENT_DURATION = 8  # Duration of each segment in seconds
TOTAL_DURATION = 20  # Duration to save when F9 is pressed
OUTPUT_DIR = "C:\\LANClips\\OneDrive\\LAN\\"
SEGMENTS_DIR = "temp_segments"

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def start_ffmpeg_recording():
    """Starts an FFmpeg process to record continuously in short segments."""
    if not os.path.exists(SEGMENTS_DIR):
        os.makedirs(SEGMENTS_DIR)

    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'gdigrab',  # Capture desktop for Windows
        '-framerate', str(FPS),
        '-offset_x', '0',  # Start at the top-left corner (0,0)
        '-offset_y', '0',
        '-video_size', f'{screensize[0]}x{screensize[1]}',  # Adjust to your main screen resolution
        '-i', 'desktop',  # Capture desktop
        '-c:v', 'libx264',
        '-preset', 'ultrafast',  # Use ultrafast preset to reduce CPU usage
        '-pix_fmt', 'yuv420p',
        '-f', 'segment',  # Use segment format to create multiple small files
        '-segment_time', str(SEGMENT_DURATION),  # Duration of each segment
        '-reset_timestamps', '1',  # Reset timestamps for each segment
        '-strftime', '1',  # Use timestamps in segment filenames
        os.path.join(SEGMENTS_DIR, 'segment_%Y%m%d%H%M%S.mp4')  # Segment file pattern
    ]

    # Start the FFmpeg process in a subprocess
    return subprocess.Popen(command)

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
    uname = os.getlogin()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    output_filename = os.path.join(OUTPUT_DIR, f"{uname}_{timestr}_clip.mp4")

    # Get the list of segment files sorted by modification time
    segment_files = sorted(glob.glob(os.path.join(SEGMENTS_DIR, 'segment_*.mp4')), key=os.path.getmtime)

    # Calculate the number of segments needed to cover at least 20 seconds
    num_segments_to_keep = (TOTAL_DURATION // SEGMENT_DURATION) + (1 if TOTAL_DURATION % SEGMENT_DURATION != 0 else 0)
    
    # Get the latest segments from the end of the list
    segment_files_to_keep = segment_files[-num_segments_to_keep:]

    # Ensure that only the segments that cover the last 20 seconds are used
    with open("segments_list.txt", "w") as f:
        for segment in segment_files_to_keep:
            f.write(f"file '{segment}'\n")

    # Use FFmpeg to concatenate the selected segments and save to output file
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'concat',
        '-safe', '0',
        '-i', 'segments_list.txt',
        '-c', 'copy',  # Copy without re-encoding to make it fast
        output_filename
    ]

    subprocess.call(command)
    print(f"Recording saved as {output_filename}")
    show_notification("Clip saved!", duration=2)

    time.sleep(2)

    # Delete old segments that are no longer needed
    segments_to_delete = segment_files[:-num_segments_to_keep]
    for segment in segments_to_delete:
        try:
            os.remove(segment)
            print(f"Deleted: {segment}")
        except Exception as e:
            print(f"Error deleting {segment}: {e}")

def main():
    print("Press F9 to save the last 20 seconds of video...")

    # Start FFmpeg in a continuous segment recording mode
    recording_process = start_ffmpeg_recording()

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
