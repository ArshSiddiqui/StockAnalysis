import termplotlib as tpl
import numpy as np

x = np.linspace(0, 2 * np.pi, 10)
y = np.sin(x)

fig = tpl.figure()
fig.plot(x, y, label="data", width=50, height=15)
fig.show()