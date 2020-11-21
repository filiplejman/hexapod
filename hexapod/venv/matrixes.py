from sympy import symbols, Matrix, cos, sin, nsolve

a, b, c = symbols('a b c')
cx, sx = symbols('cx sx')
cr, sr = symbols('cr sr')
H = symbols('H')

cp, sp = symbols('cp sp')

l1, l2, l3 = symbols('l1 l2 l3')
c2, s2 = symbols('c2 s2')
c3, s3 = symbols('c3 s3')
r, p, y = symbols('r p y')

A11 = Matrix([[cos(a + y), -sin(a + y), 0, 0], [sin((a + y)), cos((a + y)), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
A12 = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, H], [0, 0, 0, 1]])
A13 = Matrix([[1, 0, 0, 0], [0, cos(r), -sin(r), 0], [0, sin(r), cos(r), 0], [0, 0, 0, 1]])
A1 = A11 * A12 * A13

A21 = Matrix([[0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
A22 = Matrix([[1, 0, 0, 0], [0, -cos(p), sin(p), 0], [0, sin(p), -cos(p), 0], [0, 0, 0, 1]])
A2 = A21 * A22

A3 = Matrix([[1, 0, 0, l1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

A41 = Matrix([[cos(b), -sin(b), 0, 0], [sin(b), cos(b), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
A42 = Matrix([[1, 0, 0, l2], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
A4 = A41 * A42

A51 = Matrix([[cos(c), -sin(c), 0, 0], [sin(c), cos(c), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
A52 = Matrix([[1, 0, 0, l3], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
A5 = A51 * A52

T = A1 * A2 * A3 * A4 * A5

x, y, z = symbols('x y z')

x = T.row(0).col(3)[0]
y = T.row(1).col(3)[0]
z = T.row(2).col(3)[0]
print(nsolve((x, y, z), (a, b, c), (0, 0, 0)))
