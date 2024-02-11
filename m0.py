import numpy as np
import matplotlib.pyplot as plt

data = np.zeros((61, 2))

# initial popualtuogn of the 
data[:, 0] = np.arange(0, 30.5, 0.5)

for i in range(data.shape[0]):
    while True:
        user_input = input(f"Enter V_out for V_in={data[i, 0]}: ")
        try:
            data[i, 1] = float(user_input)
            break  
        except ValueError:
            print("invalid input")

print("V_in\tV_out")
for row in data:
    print(f"{row[0]:.1f}\t{row[1]:.2f}")

plt.plot(data[:, 0], data[:, 1], marker='o')
plt.xlabel('V_in')
plt.ylabel('V_out')
plt.title('Plot of V_in vs V_out')
plt.grid(True)
plt.show()
