from matplotlib import pyplot as plt
import numpy as np


def get_file_data(fname):
    pass

epochs = 100
population_size = 1024

fname = "results/ga-results-e_%d-pop_%d.txt" % (epochs, population_size)

f = open(fname, 'r')
fdata = f.read()
rows = fdata.split('\n')[:-1]

data = [[None, None] for _ in rows]


for i in range(len(rows)):
    srow = rows[i].split(",")
    data[i][0] = int(srow[0])
    data[i][1] = float(srow[1])

data = np.array(data)

# plotting
plt.plot(data[:, 0], data[:, 1], )

plt.title("GA with population %d" % population_size)
plt.xlabel("Epochs")
plt.ylabel("Fitness")

plt.grid()

plt.show()
