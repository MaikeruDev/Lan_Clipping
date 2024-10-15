# Gaming Clipping Tool for LAN Party

This Python script is designed to automatically capture the last 20 seconds of gameplay, upload the clip to OneDrive, and display a looping highlight reel on a projector at your LAN party. It uses FFmpeg to record the desktop in a continuous buffer and allows quick saves with a key press.

## Features
- **Capture the Last 20 Seconds**: The script saves the most recent 20 seconds of your screen when you press `F9`.
- **OneDrive Integration**: Automatically uploads clips to a designated folder in OneDrive for easy sharing across devices.
- **Loop on a Projector**: Another PC connected to a beamer (projector) continuously plays the clips for real-time highlights during your LAN party.
- **Customizable**: Easily configure FPS, recording duration, and save locations.

## Requirements
- **Python 3.x**
- **FFmpeg** (Make sure it's installed and added to your PATH)
- **Tkinter**: For displaying notifications.
- **keyboard**: For detecting keypresses.

## Why I Made This

The inspiration for this tool came from how often Call of Duty’s Play of the Game feature shows terrible moments, ignoring the best plays of the match. I wanted to make sure me and my boys could capture and showcase our real top moments during our LAN parties—because we all know those epic plays deserve the spotlight!

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/MaikeruDev/Lan_Clipping.git
   ```
2. Install the required Python packages:
   ```bash
   pip install keyboard tkinter
   ```

3. Install **FFmpeg**:
   - Follow instructions to download and install FFmpeg: https://ffmpeg.org/download.html
   - Add FFmpeg to your system PATH for easy command-line access.

## Configuration

- **FPS**: Default is set to 30, but you can modify it in the script based on your needs.
- **Duration**: The duration for the circular buffer is set to 20 seconds but can be changed.
- **Output Directory**: Set your desired output directory in the `OUTPUT_DIR` variable, such as a OneDrive folder.

## Usage

1. Start the script:
   ```bash
   python main.py
   ```

2. Press `F9` to save the last 20 seconds of gameplay. The clip will be saved and uploaded to OneDrive automatically.

3. On another PC connected to a beamer (projector), set up a loop to display clips in real-time as they're uploaded to OneDrive.

## Notifications
The script includes a small notification system using Tkinter to display when a clip is successfully saved. This will pop up in the bottom-right corner of your screen.

## Example Output
Saved clips will follow this naming format:
```
C:\LANClips\OneDrive\LAN\{username}_{timestamp}_clip.mp4
```

## Known Issues
- **High CPU Usage**: When using high resolutions with FFmpeg, CPU usage may increase.
- **OneDrive Sync Delay**: Ensure OneDrive syncs quickly, or there might be a delay in clips appearing on the projector.

## Contributions
Feel free to fork the repository and make improvements! Pull requests are welcome.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.
