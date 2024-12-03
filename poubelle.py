import numpy as np
import matplotlib.pyplot as plt
from scipy import signal


# g = np.sin(2 * 10 * np.pi * x) * np.exp(-x**2/100) # Sine wave
g = np.genfromtxt('data_csv_interpolee.csv', delimiter=',')[1:, :]

# Define the abscissa (x-axis)
x = np.linspace(-max(np.min(g[:,0]), np.max(g[:,0])), max(np.min(g[:,0]), np.max(g[:,0])), 10000)

# Define two functions f(x) and g(x)
dirac = np.zeros_like(x)
zero_crossings = np.where(np.diff(np.sign(x)))[0]
dirac[zero_crossings] = 1
f = dirac

value = np.interp(x, g[:, 0], g[:,1], left=0, right=0)
# Perform convolution
conv = np.convolve(f, value, mode='same')  # mode can be 'full', 'valid', or 'same'
       # Gaussian function
# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(x, f, label='f(x): Gaussian')
plt.plot(g[:, 0], g[:,1]/np.max(g[:, 1]), label='g(x): Sine wave')
plt.plot(x, value / np.max(value), label='Interpolated g(x)', linestyle='--')
plt.plot(x, conv / np.max(conv), label='Convolution', linestyle='--')  # Normalize for visualization
plt.legend()
plt.title('Convolution of f(x) and g(x)')
plt.xlabel('x')
plt.ylabel('Amplitude')
plt.show()
