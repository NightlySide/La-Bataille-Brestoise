from pgfutils import setup_figure, save
setup_figure(width=1, height=0.4, columns=1)

import numpy as np
from matplotlib import pyplot as plt

t = np.linspace(0, 10, 200)
s = 0.3 * t + 2.5 * np.cos(2 * np.pi * 0.85 * t) - 0.8

plt.plot(t, s)
plt.xlim(0, 10)
plt.grid(True)

save()
