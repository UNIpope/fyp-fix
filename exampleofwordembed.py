# importing two required module
import numpy as np
import matplotlib.pyplot as plt

# Creating a numpy array
x = [1,1,3,3,3,1]
y = [1,3,1,3,5,5]
l = ["  the","  red","  fox","  jumped", "  over", "  car"]

# Plotting point using scatter method
plt.scatter(x, y)

for i, txt in enumerate(l):
    plt.annotate(txt, (x[i], y[i]))


plt.xlim(-1,6)
plt.ylim(-1,6)

plt.show()