import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

myColors = ["#4285f4", "#ea4335", "#fbbc05", "#34a853"]

def randomize(stop=100, size=100):
    return np.random.randint(stop, size=size)


plt.scatter(x=randomize(), y=randomize(), c=randomize(), cmap=ListedColormap(myColors))
plt.colorbar()
plt.show()
