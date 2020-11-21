import numpy as np
from math import *


class DenavitHartenberg:
    def __init__(self):
        self._operations = []

    def add_operation(self, op):
        self._operations.append(op)

    def clear_operations(self):
        self._operations = []

    def print_operations(self):
        for op in self._operations:
            print("Rot z: {} | Trans z: {} | Trans x: {} | Rot x: {}".format(op[0], op[1], op[2], op[3]))

    def _transform(self, theta, d, a, alpha):
        theta_rad = radians(theta)
        alpha_rad = radians(alpha)
        transform = np.eye(4)
        if theta != 0:
            rot_theta = np.array([
                [cos(theta_rad), -sin(theta_rad), 0, 0],
                [sin(theta_rad), cos(theta_rad), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            transform = np.matmul(transform, rot_theta)
        if d != 0:
            trans_d = np.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, d],
                [0, 0, 0, 1]
            ])
            transform = np.matmul(transform, trans_d)
        if a != 0:
            trans_a = np.array([
                [1, 0, 0, a],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])
            transform = np.matmul(transform, trans_a)
        if alpha != 0:
            rot_alpha = np.array([
                [1, 0, 0, 0],
                [0, cos(alpha_rad), -sin(alpha_rad), 0],
                [0, sin(alpha_rad), cos(alpha_rad), 0],
                [0, 0, 0, 1]
            ])
            transform = np.matmul(transform, rot_alpha)
        return transform

    def calculate(self, initial_matrix=None, clear=True):
        if initial_matrix is None:
            transformation = np.eye(4)
        else:
            transformation = initial_matrix
        transformation_list = []
        for op in self._operations:
            theta, d, a, alpha = op
            transform_result = self._transform(theta, d, a, alpha)
            transformation = np.matmul(transformation, transform_result)
            transformation_list.append(transformation)
        if clear:
            self.clear_operations()
        return transformation, transformation_list


if __name__ == "__main__":
    dh = DenavitHartenberg()
    dh.add_operation([0, 10, 0, -90])
    dh.add_operation([0, 0, 0, 90])
    dh.add_operation([0, 0, 0, 0])
    ret = dh.calculate()
    print(ret)
    print(ret[0, 3])
