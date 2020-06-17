import autograd.numpy as np
import argparse
import json
import ast

from parser import parse
from utils import *


def add_assertion(args, spec):
    assertion = dict()

    assertion['robustness'] = 'local'
    assertion['distance'] = 'di'
    assertion['eps'] = '1e9' # bounds are updated so eps is not necessary

    spec['assert'] = assertion


def add_solver(args, spec):
    solver = dict()

    solver['algorithm'] = args.algorithm
    if args.algorithm == 'sprt':
        solver['threshold'] = str(args.threshold)
        solver['alpha'] = "0.05"
        solver['beta'] = "0.05"
        solver['delta'] = "0.005"

    spec['solver'] = solver


def update_bounds(args, model, x0):
    eps = np.full(x0.shape, args.eps)

    if args.dataset == 'cifar_conv':
        eps[0:1024] = eps[0:1024] / 0.2023
        eps[1024:2048] = eps[1024:2048] / 0.1994
        eps[2048:3072] = eps[2048:3072] / 0.2010
    elif args.dataset == 'mnist_conv':
        eps = eps / 0.3081

    model.lower = np.maximum(model.lower, x0 - eps)
    model.upper = np.minimum(model.upper, x0 + eps)


def main():
    np.set_printoptions(threshold=20)
    parser = argparse.ArgumentParser(description='nSolver')

    parser.add_argument('--spec', type=str, default='spec.json',
                        help='the specification file')
    parser.add_argument('--algorithm', type=str,
                        help='the chosen algorithm')
    parser.add_argument('--threshold', type=float,
                        help='the threshold in sprt')
    parser.add_argument('--eps', type=float,
                        help='the distance value')
    parser.add_argument('--dataset', type=str,
                        help='the data set for ERAN experiments')

    args = parser.parse_args()

    with open(args.spec, 'r') as f:
        spec = json.load(f)

    add_assertion(args, spec)
    add_solver(args, spec)

    model, assertion, solver = parse(spec)

    if args.dataset == 'cifar_conv':
        pathX = 'benchmark/eran/data/cifar_conv/'
        pathY = 'benchmark/eran/data/labels/y_cifar.txt'
    elif args.dataset == 'cifar_fc':
        pathX = 'benchmark/eran/data/cifar_fc/'
        pathY = 'benchmark/eran/data/labels/y_cifar.txt'
    elif args.dataset == 'mnist_conv':
        pathX = 'benchmark/eran/data/mnist_conv/'
        pathY = 'benchmark/eran/data/labels/y_mnist.txt'
    elif args.dataset == 'mnist_fc':
        pathX = 'benchmark/eran/data/mnist_fc/'
        pathY = 'benchmark/eran/data/labels/y_mnist.txt'

    y0 = np.array(ast.literal_eval(read(pathY)))

    for i in range(100):
        assertion['x0'] = pathX + 'data' + str(i) + '.txt'
        x0 = np.array(ast.literal_eval(read(assertion['x0'])))

        output_x0 = model.apply(x0)
        lbl_x0 = np.argmax(output_x0, axis=1)[0]

        if lbl_x0 == y0[i]:
            update_bounds(args, model, x0)
            print('Run at data {}'.format(i))
            solver.solve(model, assertion)
        else:
            print('Skip at data {}'.format(i))

        print('\n============================\n')


if __name__ == '__main__':
    main()
