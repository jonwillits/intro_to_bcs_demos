import numpy as np


class GHA(object):
    def __init__(self, n_features, n_input, dtype=None):
        self.n_features = n_features
        self.n_input = n_input
        self.w = np.array(np.random.rand(n_features, n_input)*2-1,dtype=dtype)
        self.dw = None
        self.error = None

    def partial_fit(self, x, nu, remember_dw = False):
        y = np.dot(self.w, x)
        dw = (np.outer(y, x) - np.dot(np.tril(np.outer(y, y)), self.w))*nu
        if remember_dw:
            self.dw = dw
        self.w += dw

def main():
    fit_data1 = np.array([[-1.76586391869932, -0.91392532736063],
                          [-1.38289715070277, -0.502829586621374],
                          [-0.618779826909304, -0.408257109113038],
                          [-0.279251442290843, -0.469211537856609],
                          [-0.617764072492719, -0.565175158903003],
                          [-1.67860568827018, -0.845086738467216],
                          [-0.611263827420771, -0.0395743944682181],
                          [0.296234296169132, -0.65233340440318],
                          [-0.81200323626399, 0.160686868242919],
                          [0.851336521562189, 0.182786221150309]], dtype=np.double)

    fit_data2 = np.array([[1, 2],
                          [3, 6],
                          [-2, -4],
                          [-1, -2],
                          [-10, -20],
                          [5, 10],
                          [4, 9],
                          [-3, -5],
                          [-8, -15],
                          [0.2, 0.4]], dtype=np.double)

    x = np.array([[1,3,-2,-1,-10,5,4,-3,-8,0.2],[2,6,-4,-2,-20,10,9,-5,-15,0.4]])

    g = GHA(2, 2)
    n, _ = fit_data2.shape
    for epoch in range(100):
        for i in range(n):
            g.partial_fit(fit_data1[i], 0.01, True)
        if epoch%1==0:
            print(epoch, g.w)
    print(np.corrcoef(x))

main()

