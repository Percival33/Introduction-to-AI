import numpy as np

     
class DlNet:
    def __init__(self, LR: float = 0.003, batch_size: int = 100, neurons: int = 7):
        self._HIDDEN_L_SIZE = neurons
        self._LR = LR

        self._y = np.zeros(self._HIDDEN_L_SIZE)
        self.y_out = 0

        self._batch_size = batch_size
        self._iter_count = 0
        
        self._hidden_weight = np.random.normal(size=self._HIDDEN_L_SIZE)
        self._hidden_bias = np.random.normal(size=self._HIDDEN_L_SIZE)
        self._output_weight = np.random.normal(size=self._HIDDEN_L_SIZE)
        self._output_bias = np.random.normal()

        self._derivative_hidden_weight = np.zeros(self._HIDDEN_L_SIZE)
        self._derivative_hidden_bias = np.zeros(self._HIDDEN_L_SIZE)
        self._derivative_output_weight = np.zeros(self._HIDDEN_L_SIZE)
        self._derivative_output_bias = 0
        
        self._loss_values = []
        self._step = 100

    def forward(self, x: float):
        self._y = self.sigmoid(self._hidden_weight * x + self._hidden_bias)
        self.y_out = sum(self._output_weight * self._y) + self._output_bias

    def predict(self, x: float) -> float:
        y = self.sigmoid(self._hidden_weight * x + self._hidden_bias)
        return sum(self._output_weight * y) + self._output_bias

    def backward(self, x: float, y: float):
        # output layer
        self._derivative_output_weight += self.d_nloss(self.y_out, y) * self._y
        self._derivative_output_bias += self.d_nloss(self.y_out, y) * 1
        
        # hidden layer
        # hidden layer weights
        tmp_d = self.d_nloss(self.y_out, y) * self._output_weight
        self._derivative_hidden_weight += tmp_d * self.d_sigmoid(self._y) * x

        # hidden layer bias
        tmp_d = self.d_nloss(self.y_out, y)
        self._derivative_hidden_bias += tmp_d * self.d_sigmoid(self._y)

        self._iter_count += 1

        if self._iter_count == self._batch_size:
            # update weights and biases (gradient descent)
            self._hidden_weight -= self._LR * self._derivative_hidden_weight / self._batch_size
            self._hidden_bias -= self._LR * self._derivative_hidden_bias / self._batch_size

            self._output_weight -= self._LR * self._derivative_output_weight / self._batch_size
            self._output_bias -= self._LR * self._derivative_output_bias / self._batch_size

            # clear derivatives
            self._derivative_output_weight = np.zeros(self._HIDDEN_L_SIZE)
            self._derivative_output_bias = 0
            self._derivative_hidden_weight = np.zeros(self._HIDDEN_L_SIZE)
            self._derivative_hidden_bias = np.zeros(self._HIDDEN_L_SIZE)

            self._iter_count = 0

    def train(self, x_set: np.array, y_set: np.array, iters: int) -> None:
        loss = 0
        count = -1
        for i in range(iters):
            for x, y in zip(x_set, y_set):
                self.forward(x)
                self.backward(x, y)
                loss += self.nloss(self.y_out, y)
            count += 1
            if count == self._step:
                self._loss_values.append((i, loss / self._step))
                loss = 0
                count = 0

    def loss_func_values(self):
        return self._loss_values

    # f logistyczna jako przykład sigmoidalej
    @staticmethod
    def sigmoid(x: float) -> float:
        return 1 / (1 + np.exp(-x))

    # pochodna fun. 'sigmoid'
    @staticmethod
    def d_sigmoid(x: float) -> float:
        s = 1 / (1 + np.exp(-x))
        return s * (1 - s)

    # f. straty
    @staticmethod
    def nloss(y_out: float, y: float) -> float:
        return (y_out - y) ** 2

    # pochodna f. straty
    @staticmethod
    def d_nloss(y_out: float, y: float) -> float:
        return 2 * (y_out - y)
