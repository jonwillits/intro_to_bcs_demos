import numpy as np

data = np.array([[1, 2],
                [3, 6],
                      [-2, -4],
                      [-1, -2],
                      [-10, -20],
                      [5, 10],
                      [4, 9],
                      [-3, -5],
                      [-8, -15],
                      [0.2, 0.4]], dtype=np.double)

w = np.random.random([2, 2])

u = 0.01
V = np.dot(w, data.T)
i = 0

for d in data:
    v = V[:, i].reshape((2, 1))  #n_features is # of columns
    w += (d * v) - u * np.square(v) * w
    i += 1

print(w)