import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Use the TkAgg backend for interactive plots
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from scipy.fft import fft, fftfreq
from scipy.fft import fftshift
from scipy.signal import detrend
csv='out_500.csv'

mycsv=csv
# Channel names
channels = ['CH' + str(i) for i in range(1, 13)]

# Create the main window
root = tk.Tk()
root.title('Channel Selection')
scan_enable = True
fft_enable = True
def browse_file():
    filename = filedialog.askopenfilename(
        initialdir="/", 
        title="Select a File", 
        filetypes=(("Text files", "*.csv"), ("all files", "*.*"))
    )
    # Update the label with the file name
    # label_file_explorer.configure(text="File Opened: " + filename)
    global csv
    # print(len(filename))
    if len(filename) > 2:
        csv=filename
        print(csv)
# Create a dictionary to store the checkbox variables
checkbox_vars = {channel: tk.BooleanVar(root) for channel in channels}
radio_var = tk.BooleanVar(root, value=True)
radio_var1 = tk.BooleanVar(root, value=False)
# Create a button to browse files

def plot():
    for channel, var in checkbox_vars.items():
        if var.get():
            # Apply the filter
            # print(channel)
            # if channel == 'CH12':
            if radio_var.get():
                scan_enable = True
            else:
                scan_enable = False
            if radio_var1.get():
                fft_enable = True
            else:
                fft_enable = False
            # print(csv)
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

# Assuming butter_lowpass_filter and scan_and_adjust_axes are defined elsewhere in your code

def plot_signal(filename, column_name, scan_enabled, fft_enabled):
    # Load the CSV file
    data = pd.read_csv(filename)

    # Extract the 'counter' and the specified column
    x = data['Counter']
    y = data[column_name]

    # Calculate the time for each sample
    fs = 30000  # sampling rate, Hz
    time = x / fs

    # Apply lowpass filter
    cutoff = 5000  # desired cutoff frequency of the filter, Hz
    y_filtered = butter_lowpass_filter(y, cutoff, fs)

    # Detrend and remove DC offset from the filtered signal
    y_detrended = detrend(y_filtered)
    y_detrended -= np.mean(y_detrended)

    # Perform FFT on the detrended signal
    yf = fft(y_detrended)
    xf = fftfreq(len(y_detrended), 1 / fs)

    # Use fftshift to center the zero frequency
    yf_shifted = fftshift(yf)
    xf_shifted = fftshift(xf)

    # Find the peak frequency, excluding the zero frequency component
    idx_peak = np.argmax(np.abs(yf_shifted[len(yf_shifted)//2+1:])) + len(yf_shifted)//2 + 1
    peak_freq = xf_shifted[idx_peak]

    plt.figure()
    if fft_enabled == True:
        # plt.figure(figsize=(10, 6))
    # Plot the FFT result on a separate figure
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

        # plt.show()

        # plt.figure(figsize=(10, 6))
    plt.plot(time, y_filtered, label=column_name, color='red')
    plt.xlabel('Time (s)')
    plt.ylabel(column_name)

    # Scan the x and y axes to get the best view
    # print(scan_enable)
    if scan_enabled == True:
        scan_and_adjust_axes(time, y)
        plt.title('Signal '+ column_name+ " (Scan enabled)", color='green')
    else:
        plt.title('Signal '+ column_name+ " (Raw Data)", color='green')
        plt.annotate(f'Peak Frequency: {peak_freq:.2f} Hz',
                xy=(time[idx_peak], y_filtered[idx_peak]),
                xytext=(time[idx_peak]+0.1, y_filtered[idx_peak]),
                arrowprops=dict(facecolor='blue', shrink=0.05))
    plt.text(0.9, -0.1, f'Peak Frequency: {peak_freq:.2f} Hz',
             fontsize=14, fontweight='bold', ha='center', va='center', transform=plt.gca().transAxes)
    plt.legend()
    plt.grid()
    plt.show()

# Remember to call the function with the appropriate arguments
# plot_signal('your_data.csv', 'YourColumnName', True or False)



def scan_and_adjust_axes(x, y):
    # Find the x and y values where the signal is the strongest
    max_y = max(y)
    max_x = x[np.argmax(y)]  # Use np.argmax() to find the index of the max y value
    # print(max_x)
    # Adjust the x-axis limits to focus on the strongest part of the signal
    plt.xlim(max_x - max_x/152, max_x + max_x/152)  # Adjust these values as needed

# Create checkboxes for each channel
for channel in channels:
    tk.Checkbutton(root, text=channel, variable=checkbox_vars[channel]).pack()

# Create the plot button
tk.Button(root, text='Plot', command=plot).pack()
# Add radio buttons for enabling and disabling the scan and adjust function
tk.Radiobutton(root, text='Auto', variable=radio_var, value=True).pack()
tk.Radiobutton(root, text='RAW', variable=radio_var, value=False).pack()
tk.Radiobutton(root, text='Show FFT', variable=radio_var1, value=True).pack()
tk.Radiobutton(root, text='Hide FFT', variable=radio_var1, value=False).pack()
button_explore = tk.Button(root, text="Browse Files", command=browse_file).pack()
# button_explore.grid(column=1, row=2)
# Start the main loop
root.mainloop()