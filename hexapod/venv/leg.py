from denavit_hartenberg import DenavitHartenberg
from point import Point, Operation
from math import *


class Leg:

    def __init__(self, name, coxa, femur, tibia, origin, translation=None, coxa_max=120, femur_max=120, tibia_max=120):
        self.name = name
        self.femur = femur
        self.tibia = tibia
        self.coxa = coxa
        self.origin = origin
        self.origin_matrix = translation
        self.coxa_max = coxa_max
        self.femur_max = femur_max
        self.tibia_max = tibia_max
        self.effector = Point(25, 0, 0)
        self.joints_self = []
        self.joints_origin = []
        self.inverse_kin(origin, self.origin_matrix)

    def inverse_kin(self, current_origin, origin_matrix=None):
        self.calculate_effector(current_origin)
        H = current_origin.z - self.effector.z
        D2 = pow(self.effector.x, 2) + pow(self.effector.y, 2) + pow(H, 2)
        E2 = pow(self.coxa.length, 2) + D2 - 2*self.coxa.length*sqrt(D2-pow(H, 2))
        c3 = (E2 - pow(self.femur.length, 2) - pow(self.tibia.length, 2)) / (2*self.femur.length*self.tibia.length)
        self.coxa.angle = atan2(self.effector.y, self.effector.x)
        self.coxa.angle = degrees(self.coxa.angle)
        self.tibia.angle = atan2(sqrt(1-pow(c3, 2)), c3)
        self.tibia.angle = degrees(self.tibia.angle)
        self.femur.angle = atan2(H, sqrt(E2 - pow(H, 2))) - acos((E2 + pow(self.femur.length, 2)
                                                                  - pow(self.tibia.length, 2)) /
                                                                 (2*self.femur.length*sqrt(E2)))
        self.femur.angle = degrees(self.femur.angle)
        self.simple_kin(origin_matrix)

    def calculate_effector(self, current_origin):
        dx = self.origin.x - current_origin.x
        dy = self.origin.y - current_origin.y
        self.effector.x += dx
        self.effector.y += dy

    def simple_kin(self, origin_matrix=None):
        dh = DenavitHartenberg()
        if origin_matrix is not None:
            dh.add_operation([self.coxa.angle, 0, self.coxa.length, -90])
            dh.add_operation([self.femur.angle, 0, self.femur.length, 0])
            dh.add_operation([self.tibia.angle, 0, self.tibia.length, 0])
        else:
            dh.add_operation([self.coxa.angle, self.origin.z, 0, -90])
            dh.add_operation([self.femur.angle, 0, self.femur.length, 0])
            dh.add_operation([self.tibia.angle, 0, self.tibia.length, 0])

        dh_matrix, dh_operations = dh.calculate(origin_matrix)
        self.joints_origin = [self.get_point_data(_) for _ in dh_operations]
        sub_point = self.get_point_data(origin_matrix)
        sub_point.operation(Point(self.origin.x, self.origin.y, 0), op=Operation.SUBTRACT)
        self.joints_origin.insert(0, sub_point)
        dh.add_operation([self.coxa.angle, self.origin.z, 0, -90])
        dh.add_operation([self.femur.angle, 0, self.femur.length, 0])
        dh.add_operation([self.tibia.angle, 0, self.tibia.length, 0])
        dh_matrix, dh_operations = dh.calculate()
        self.joints_self = [self.get_point_data(_) for _ in dh_operations]

    def get_point_data(self, dh_matrix):
        x = dh_matrix[0, 3]
        y = dh_matrix[1, 3]
        z = dh_matrix[2, 3]
        return Point(x, y, z)

    def set_origin(self, new_origin):
        self.origin = new_origin

    def __str__(self):
        s = "Parameters of " + self.name + ":\n"
        s += "============================== \n"
        s += "Coxa length: " + str(self.coxa.length) + " | angle: " + str(self.coxa.angle) + "\n"
        s += "Femur length: " + str(self.femur.length) + " | angle: " + str(self.femur.angle) + "\n"
        s += "Tibia length: " + str(self.tibia.length) + " | angle: " + str(self.tibia.angle) + "\n"
        # s += "============================== \n"
        # s += "Joints coordinates \n"
        # for cnt, joint in enumerate(self.joints_self):
        #     s += "Joint " + str(cnt) + ": " + joint.__str__() + "\n"
        # s += "============================== \n"
        s += "Effector " + "\n" + self.effector.__str__() + "\n"
        s += "============================== \n"
        return s


class Joint:
    def __init__(self, angle, length):
        self.angle = angle
        self.length = length

    def __str__(self):
        return "length: " + str(self.length) + " | angle: " + str(self.angle)


if __name__ == "__main__":
    l1 = Leg("sample_leg", Joint(90, 5), Joint(90, 10), Joint(0, 10), Point(0, 0, 20))
    # print(l1)
    # l1.effector = Point(5, 0, 1)
    # l1.inverse_kin(Point(0, 0, 0))
    print(l1)
    print(l1.joints_self)
