import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Generate a noisy square wave signal
fs = 30000 # Sampling frequency in Hz
t = np.arange(0, 1, 1/fs) # Time array in seconds
f = 1000 # Signal frequency in Hz
x = np.sign(np.sin(2*np.pi*f*t)) # Square wave signal
noise = np.random.normal(0, 0.5, len(t)) # Gaussian noise
y = x + noise # Noisy signal

# Design a low-pass filter with a cutoff frequency of 5 kHz
fc = 5000 # Cutoff frequency in Hz
w = fc / (fs / 2) # Normalized cutoff frequency
b, a = butter(4, w, "low") # 4th order low-pass filter

# Apply the filter to the noisy signal
z = lfilter(b, a, y)

# Plot the signals
plt.figure(figsize=(10, 6))
plt.subplot(211)
plt.plot(t, y, label="Noisy signal")
plt.plot(t, x, label="Original signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.subplot(212)
plt.plot(t, z, label="Filtered signal")
plt.plot(t, x, label="Original signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.show()
