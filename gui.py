import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, detrend, lfilter
from scipy.fft import fft, fftfreq, fftshift
csv = 'out_500.csv'

# Initialize the main window
root = tk.Tk()
root.title('Signal Viewer')

# Define the channels
channels = ['CH' + str(i) for i in range(1, 13)]

# Define the style for the ttk widgets
style = ttk.Style()
# style.configure('TButton', font=('Arial', 10), background='blue', foreground='white')
# style.configure('TRadiobutton', font=('Arial', 10))
# style.configure('TCheckbutton', font=('Arial', 10))
# Rem above lines for better button view in windows

# Function to browse and select a file
def browse_file():
    filename = filedialog.askopenfilename(
        initialdir="/",
        title="Select",
        filetypes=(("CSV files", "*.csv"), ("all files", "*.*"))
    )
    global csv
    if len(filename) > 2:
        csv = filename
        print(csv)

# Function to plot the signal
def plot_signal(csv_filename, channel, scan, fft_show):
    # Your existing signal plotting code here
    # For demonstration, let's create a simple plot
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    # Embed the plot into the Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Function to handle the plot action
def plot():
    for channel, var in checkbox_vars.items():
        if var.get():
            scan_enable = radio_var.get()
            fft_enable = radio_var1.get()
            plot_signal(csv, channel, scan_enable, fft_enable)


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

def plot_signal(filename, column_name, scan_enabled, fft_enabled):
    data = pd.read_csv(filename)

    x = data['Counter']
    y = data[column_name]

    fs = 30000
    time = x / fs

    cutoff = 5000
    y_filtered = butter_lowpass_filter(y, cutoff, fs)

    # # Design a low-pass filter with a cutoff frequency of 5 kHz
    # fc = 5000 # Cutoff frequency in Hz
    # w = fc / (fs / 2) # Normalized cutoff frequency
    # b, a = butter(4, w, "low") # 4th order low-pass filter

    # # Apply the filter to the noisy signal
    # y_filtered = lfilter(b, a, y_filtered)

    y_detrended = detrend(y_filtered)
    y_detrended -= np.mean(y_detrended)

    yf = fft(y_detrended)
    xf = fftfreq(len(y_detrended), 1 / fs)

    yf_shifted = fftshift(yf)
    xf_shifted = fftshift(xf)

    idx_peak = np.argmax(np.abs(yf_shifted[len(yf_shifted)//2+1:])) + len(yf_shifted)//2 + 1
    peak_freq = xf_shifted[idx_peak]

    plt.figure()
    if fft_enabled == True:
        # plt.figure(figsize=(10, 6))
        plt.plot(xf_shifted, np.abs(yf_shifted))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.title(f'FFT of {column_name}')
        plt.annotate(f'Peak Frequency: {peak_freq:.2f} Hz',
                    xy=(peak_freq, np.abs(yf_shifted[idx_peak])),
                    xytext=(peak_freq+1000, np.abs(yf_shifted[idx_peak])),
                    arrowprops=dict(facecolor='blue', shrink=0.05))
        plt.grid()
        plt.figure()


    plt.plot(time, y_filtered, label=column_name, color='red')
    plt.xlabel('Time (s)')
    plt.ylabel(column_name)

    if scan_enabled == True:
        scan_and_adjust_axes(time, y)
        plt.title('Signal '+ column_name+ " (Scan enabled)", color='green')
    else:
        plt.title('Signal '+ column_name+ " (Raw Data)", color='green')
        plt.annotate(f'Peak Frequency: {peak_freq:.2f} Hz',
                xy=(time[idx_peak], y_filtered[idx_peak]),
                xytext=(time[idx_peak]+0.1, y_filtered[idx_peak]),
                arrowprops=dict(facecolor='blue', shrink=0.05))
    plt.text(0.9, -0.1, f'Peak Freq.: {peak_freq:.2f} Hz',
             fontsize=12, fontweight='bold', ha='center', va='center', transform=plt.gca().transAxes)
    plt.legend()
    plt.grid()
    plt.show()

def scan_and_adjust_axes(x, y):
    max_y = max(y)
    min_y = min(y)
    max_x = x[np.argmax(y)] 
    print(max_y)
    plt.xlim(max_x - max_x/152, max_x + max_x/152)
    plt.ylim(max_y, min_y)

    # plt.xlim(max_x - max_x/152, max_x + max_x/152)
# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X)

# Create checkboxes for each channel
checkbox_vars = {channel: tk.BooleanVar(root) for channel in channels}
for channel in channels:
    ttk.Checkbutton(button_frame, text=channel, variable=checkbox_vars[channel]).pack(side=tk.LEFT)

# Create plot button
ttk.Button(button_frame, text='Plot', command=plot).pack(side=tk.LEFT)

# Create radio buttons for scan options
radio_var = tk.BooleanVar(root, value=True)
ttk.Radiobutton(button_frame, text='Auto', variable=radio_var, value=True).pack(side=tk.LEFT)
ttk.Radiobutton(button_frame, text='RAW', variable=radio_var, value=False).pack(side=tk.LEFT)

# Create radio buttons for FFT options
radio_var1 = tk.BooleanVar(root, value=False)
ttk.Radiobutton(button_frame, text='Show FFT', variable=radio_var1, value=True).pack(side=tk.LEFT)
ttk.Radiobutton(button_frame, text='Hide FFT', variable=radio_var1, value=False).pack(side=tk.LEFT)

# Create the file browse button
ttk.Button(button_frame, text="Browse Files", command=browse_file).pack(side=tk.LEFT)

# Run the main loop
root.mainloop()
