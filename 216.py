import numpy as np
import matplotlib.pyplot as plt

# Define the range of n
n = np.arange(-2, 9)

# Define x[n] using a piecewise definition
x = np.piecewise(n, [n < 2, n >= 2], [0, lambda n: (-2)**n])

# Define y[n] based on x[n] and the condition of u[6-n]
y = np.piecewise(n, [n < 2, (n >= 2) & (n <= 6), n > 6], [0, lambda n: (-2)**n, 0])

# Plot x[n]
plt.stem(n, x, use_line_collection=True, basefmt=" ", linefmt='C0-', markerfmt='C0o')
plt.title('Signal x[n] = $(-2)^n u[n-2]$')
plt.xlabel('n')
plt.ylabel('x[n]')
plt.grid(True)
plt.show()

# Plot y[n]
plt.stem(n, y, use_line_collection=True, basefmt=" ", linefmt='C1-', markerfmt='C1o')
# plt.title('Signal y[n] =#
