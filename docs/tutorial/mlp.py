""" Simple multi-layer perception neural network using Minpy """
import sys
import argparse

import minpy
import minpy.numpy as np
from minpy.nn import layers
from minpy.nn.model import ModelBase
from minpy.nn.solver import Solver
from minpy.nn.io import NDArrayIter
from examples.utils.data_utils import get_CIFAR10_data


class TwoLayerNet(ModelBase):
    def __init__(self,
                 input_size=3 * 32 * 32,
                 hidden_size=512,
                 num_classes=10):
        super(TwoLayerNet, self).__init__()
        self.add_param(name='w1', shape=(input_size, hidden_size))\
            .add_param(name='b1', shape=(hidden_size,))\
            .add_param(name='w2', shape=(hidden_size, num_classes))\
            .add_param(name='b2', shape=(num_classes,))

    def forward(self, X):
        y1 = layers.affine(X, self.params['w1'], self.params['b1'])
        y2 = layers.relu(y1)
        y3 = layers.affine(y2, self.params['w2'], self.params['b2'])
        return y3

    def loss(self, predict, y):
        return layers.softmax_loss(predict, y)

def main(args):
    model = TwoLayerNet()
    data = get_CIFAR10_data(args.data_dir)
    # reshape all data to matrix
    data['X_train'] = data['X_train'].reshape([data['X_train'].shape[0], 3 * 32 * 32])
    data['X_val'] = data['X_val'].reshape([data['X_val'].shape[0], 3 * 32 * 32])
    data['X_test'] = data['X_test'].reshape([data['X_test'].shape[0], 3 * 32 * 32])

    train_dataiter = NDArrayIter(data['X_train'],
                         data['y_train'],
                         batch_size=100,
                         shuffle=True)

    test_dataiter = NDArrayIter(data['X_test'],
                         data['y_test'],
                         batch_size=100,
                         shuffle=False)

    solver = Solver(model,
                    train_dataiter,
                    test_dataiter,
                    num_epochs=10,
                    init_rule='xavier',
                    update_rule='sgd_momentum',
                    optim_config={
                        'learning_rate': 1e-4,
                        'momentum': 0.9
                    },
                    verbose=True,
                    print_every=20)
    solver.init()
    solver.train()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Multi-layer perceptron example using minpy operators")
    parser.add_argument('--data_dir',
                        type=str,
                        required=True,
                        help='Directory that contains cifar10 data')
    main(parser.parse_args())
