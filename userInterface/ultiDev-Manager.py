import tkinter as tk
from tkinter import ttk

class DeviceManagerApp:
    def __init__(self, root):
        root.title("Device Manager")
        root.geometry("1200x800")

        # Main frame to contain everything
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        # Top frame for Overall Statistics and Control Buttons
        top_frame = tk.Frame(main_frame, height=100, bg="lightgray", padx=10, pady=10)
        top_frame.pack(fill="x")

        # Overall Statistics label
        self.stats_label = tk.Label(top_frame, text="Overall Statistics: Connected devices, functions, program status", font=("Arial", 12))
        self.stats_label.pack(anchor="w")

        # Top control buttons
        self.create_top_buttons(top_frame)

        # Middle frame for Device List and Controls
        middle_frame = tk.Frame(main_frame, padx=10, pady=10)
        middle_frame.pack(fill="both", expand=True)

        # Device List frame (Scrollable)
        device_list_frame = tk.Frame(middle_frame, width=400, height=600, bg="white")
        device_list_frame.pack(side="left", fill="y")

        # Scrollable Canvas for Device List
        device_canvas = tk.Canvas(device_list_frame, bg="white")
        scrollbar = ttk.Scrollbar(device_list_frame, orient="vertical", command=device_canvas.yview)
        self.device_frame = tk.Frame(device_canvas, bg="white")

        # Configure canvas and scrollbar
        device_canvas.create_window((0, 0), window=self.device_frame, anchor="nw")
        device_canvas.config(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        device_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind canvas to scroll
        self.device_frame.bind("<Configure>", lambda e: device_canvas.configure(scrollregion=device_canvas.bbox("all")))

        # Populate with sample device panels
        self.populate_device_list()

        # Frame for Device Details/Settings and Terminal/Control
        control_frame = tk.Frame(middle_frame, bg="lightblue", width=400)
        control_frame.pack(side="right", fill="both", expand=True)

        # Panel to show device details or settings
        self.device_info_label = tk.Label(control_frame, text="Device Info / Settings Panel", font=("Arial", 12))
        self.device_info_label.pack(anchor="w", padx=5, pady=5)
        self.device_info_text = tk.Text(control_frame, height=15, font=("Courier", 10), state="disabled")
        self.device_info_text.pack(fill="x", padx=10, pady=10)

        # Bottom frame for Settings Summary
        settings_frame = tk.Frame(main_frame, height=100, bg="lightgray", padx=10, pady=10)
        settings_frame.pack(fill="x")

        settings_label = tk.Label(settings_frame, text="Settings Summary: Configure appearance, update intervals, etc.", font=("Arial", 12))
        settings_label.pack(anchor="w")

    def create_top_buttons(self, parent):
        """Create top control buttons for additional functions."""
        button_frame = tk.Frame(parent, bg="lightgray")
        button_frame.pack(anchor="e")

        # Button 1: Open Terminal Window
        terminal_button = tk.Button(button_frame, text="Open Terminal", command=self.open_terminal_window)
        terminal_button.pack(side="left", padx=5)

        # Button 2: Connect to Device Screen
        connect_button = tk.Button(button_frame, text="Connect to Screen", command=self.connect_to_device_screen)
        connect_button.pack(side="left", padx=5)

        # Button 3: Manage All Devices
        manage_button = tk.Button(button_frame, text="Manage Devices", command=self.manage_all_devices)
        manage_button.pack(side="left", padx=5)

        # Button 4: Open Settings Window
        settings_button = tk.Button(button_frame, text="Settings", command=self.open_settings_window)
        settings_button.pack(side="left", padx=5)

    def populate_device_list(self):
        """Create a sample list of devices that are scrollable."""
        sample_devices = [("Device #1", "192.168.1.2"), ("Device #2", "192.168.1.3"), ("Device #3", "192.168.1.4")]

        for device_name, ip in sample_devices:
            # Frame for each device
            device_frame = tk.Frame(self.device_frame, padx=5, pady=5, bd=1, relief="solid")
            device_frame.pack(fill="x", pady=2)

            # Display device name and IP
            device_label = tk.Label(device_frame, text=f"{device_name}\nIP: {ip}\nStatus: Online", font=("Arial", 10))
            device_label.pack(anchor="w")

            # Device actions
            action_button = tk.Button(device_frame, text="Details", command=lambda d=device_name: self.show_device_info(d))
            action_button.pack(side="left", padx=5)

            lock_button = tk.Button(device_frame, text="Lock Device")
            lock_button.pack(side="left", padx=5)

    def show_device_info(self, device_name):
        """Show detailed info for a device in the side panel."""
        info_text = f"Device: {device_name}\nIP Address: ...\nUp Time: ...\nLast Online: ..."
        self.device_info_text.config(state="normal")
        self.device_info_text.delete(1.0, tk.END)
        self.device_info_text.insert(tk.END, info_text)
        self.device_info_text.config(state="disabled")

    def open_terminal_window(self):
        """Open a new window with a built-in terminal."""
        terminal_window = tk.Toplevel()
        terminal_window.title("Terminal")
        terminal_window.geometry("600x400")

        terminal_label = tk.Label(terminal_window, text="Terminal", font=("Arial", 14))
        terminal_label.pack(anchor="w", padx=10, pady=10)

        terminal_text = tk.Text(terminal_window, height=20, font=("Courier", 10))
        terminal_text.pack(fill="both", expand=True, padx=10, pady=10)

    def connect_to_device_screen(self):
        """Open a device selection menu for screen sharing."""
        connect_window = tk.Toplevel()
        connect_window.title("Connect to Device Screen")
        connect_window.geometry("400x300")

        tk.Label(connect_window, text="Select Device to Connect:", font=("Arial", 12)).pack(pady=10)

        devices = ["Device #1", "Device #2", "Device #3"]
        for device in devices:
            tk.Button(connect_window, text=device, command=lambda d=device: self.connect_to_screen(d)).pack(pady=5)

    def connect_to_screen(self, device_name):
        """Connect to a device's screen (placeholder for actual functionality)."""
        print(f"Connecting to {device_name}'s screen...")

    def manage_all_devices(self):
        """Use the side panel to manage settings for all devices."""
        self.device_info_text.config(state="normal")
        self.device_info_text.delete(1.0, tk.END)
        self.device_info_text.insert(tk.END, "Managing all devices:\n- Set global parameters\n- Lock/unlock all\n...")
        self.device_info_text.config(state="disabled")

    def open_settings_window(self):
        """Open the settings window with configuration options."""
        settings_window = tk.Toplevel()
        settings_window.title("Settings")
        settings_window.geometry("400x400")

        settings_label = tk.Label(settings_window, text="Settings", font=("Arial", 14))
        settings_label.pack(anchor="w", padx=10, pady=10)

        settings_options = ["Update interval", "Font color", "Background color", "Other options..."]
        for option in settings_options:
            tk.Label(settings_window, text=option).pack(anchor="w", padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = DeviceManagerApp(root)
    root.mainloop()
