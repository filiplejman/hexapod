from denavit_hartenberg import DenavitHartenberg
from point import Point, Operation


class Body:
    def __init__(self, parameters, center, roll, pitch, yaw):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
        self.center = center
        self.dh = DenavitHartenberg()
        self.corners_data = list(parameters)
        self.corners = []
        self.calculate_body(Point(0, 0, 0), 0, 0, 0)

    def _calculate_corners_matrix(self):
        self.dh.add_operation([self.yaw, self.center.z, self.center.x, -90])
        self.dh.add_operation([self.pitch, self.center.y, 0, 90])
        self.dh.add_operation([0, 0, 0, self.roll])
        dh_matrix, _ = self.dh.calculate()
        return dh_matrix

    def _calculate_corner(self, corners_matrix, corner_data):
        self.dh.add_operation([corner_data[0], 0, corner_data[1], 0])
        dh_matrix, _ = self.dh.calculate()
        corner_matrix = corners_matrix.dot(dh_matrix)
        corner_x = corner_matrix[0, 3]
        corner_y = corner_matrix[1, 3]
        corner_z = corner_matrix[2, 3]
        return Point(corner_x, corner_y, corner_z), corner_matrix

    def calculate_body(self, p, roll, pitch, yaw):
        self.center.operation(p, Operation.ADD)
        self.roll += roll
        self.pitch += pitch
        self.yaw += yaw
        corners_matrix = self._calculate_corners_matrix()
        self.corners = [self._calculate_corner(corners_matrix, self.corners_data[n]) for n in range(6)]

    def __str__(self):

        s = "Body data: \n"
        for cnt, corner in enumerate(self.corners):
            s += "Corner " + str(cnt) + "\n"
            s += corner[0].__str__() + "\n"
        return s


if __name__ == "__main__":
    rot = (
        0,
        60,
        120,
        180,
        240,
        300
    )

    len = [
        15,
        15,
        15,
        15,
        15,
        15
    ]
    b = Body(zip(rot, len), Point(0, 0, 0), 360, 0, 0)
    print(b)
