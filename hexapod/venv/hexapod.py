from leg import Leg, Joint
from point import Point
from body import Body


class Hexapod:

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

    def __init__(self):
        names = [
            "l1",
            "l2",
            "l3",
            "r1",
            "r2",
            "r3"
        ]
        self.centre = Point(0, 0, 5)
        self.pitch = 0
        self.roll = 0
        self.yaw = 0
        self.body = Body(zip(self.rot, self.len), self.centre, 0, 0, 0)
        self.legs = [Leg(names[n], Joint(0, 5), Joint(-90, 10), Joint(130, 23), self.body.corners[n][0],
                         self.body.corners[n][1]) for n in range(6)]
        print(self)

    def __str__(self):
        s = "---Hexapod---\n"
        s += self.body.__str__()
        for cnt, leg in enumerate(self.legs):
            s += "Leg " + str(cnt) + "\n"
            s += leg.__str__()
        return s

    def translate(self, x, y, z):
        pass

    def rotate(self, a, b, c):
        pass

    def trajectory(self, fnc):
        pass

    def update_configuration(self, p, dr=0, dp=0, dy=0):
        self.body.calculate_body(p, dr, dp, dy)
        for l, c in zip(self.legs, self.body.corners):
            # print(l)
            l.inverse_kin(current_origin=c[0], origin_matrix=c[1])
        print(self)


if __name__ == "__main__":
    hexapod = Hexapod()
    print(hexapod)
