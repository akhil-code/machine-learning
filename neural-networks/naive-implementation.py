from numpy import abs, array, dot, exp, mean, random, transpose

class NeuralNetwork:
    def __init__(self,iterations=100000):
        self.iterations = iterations
        random.seed(1)

        """ 3 layers: 3, 5, 1 """
        # weights
        self.w0 = 2*random.random((3, 5)) - 1
        self.w1 = 2*random.random((5, 1)) - 1

        # input and output arrays
        self.x = array([
            [0, 0, 1],
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 1],
        ])

        self.y = array([
            [0],
            [1],
            [1],
            [0],
        ])
    
    def f(self, x, derivative=False):
        if derivative:
            return x*(1 - x)
        return 1 / (1 + exp(-x))
    
    def train(self):
        for i in range(self.iterations):
            self.l0 = self.x
            self.l1 = self.f(dot(self.l0, self.w0))
            self.l2 = self.f(dot(self.l1, self.w1))

            self.l2_error = self.y - self.l2
            self.l2_delta = self.l2_error * self.f(self.l2, derivative=True)

            self.l1_error = self.l2_delta * transpose(self.w1)
            self.l1_delta = self.l1_error * self.f(self.l1, derivative=True)

            self.w1 += dot(transpose(self.l1), self.l2_delta)
            self.w0 += dot(transpose(self.l0), self.l1_delta)

            if( i % (self.iterations/10) == 0):
                output = f"Error: {mean(abs(self.l2_error))}"
                print(output)
    
    def predict(self, x):
        l0 = x
        l1 = self.f(dot(l0, self.w0))
        l2 = self.f(dot(l1, self.w1))
        return l2

ann = NeuralNetwork(iterations=1000000)
ann.train()
print(ann.predict(array([[1, 1, 1]])))
print(ann.predict(array([[1, 0, 1]])))
print(ann.predict(array([[0, 0, 1]])))