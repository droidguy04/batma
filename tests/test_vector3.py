import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class Test_Vector3(unittest.TestCase):
    def get_target(self, *args, **kwargs):
        from batma.maths.algebra import Vector3
        return Vector3(*args, **kwargs)

    def test_init_no_param(self):
        v = self.get_target()
        assert v.x == 0
        assert v.y == 0
        assert v.z == 0

    def test_init(self):
        v = self.get_target(5, 10, 2)
        assert v.x == 5
        assert v.y == 10
        assert v.z == 2

    def test_init_propertys(self):
        from batma.maths.algebra import Vector3
        
        v = Vector3.Zero
        assert v.x == 0
        assert v.y == 0
        assert v.z == 0

        v = Vector3.One
        assert v.x == 1
        assert v.y == 1
        assert v.z == 1

    def test_list(self):
        v = self.get_target(5, 6, 3)
        assert v[0] == 5
        assert v[1] == 6
        assert v[2] == 3

    def test_copy(self):
        v1 = self.get_target(2, 3, 1)
        assert v1.copy == v1.__copy__
        assert v1.__pos__ == v1.__copy__

        v2 = v1.copy()
        assert v1 is not v2
        assert v2.x == 2
        assert v2.y == 3
        assert v2.z == 1

    def test_eq(self):
        v = self.get_target(3, 4, 1)
        assert v == self.get_target(3, 4, 1)
        assert v == [3, 4, 1]

    def test_ne(self):
        assert self.get_target(3, 4, 2) != self.get_target(2, 3, 2)
        assert not self.get_target(3, 4, 1) != self.get_target(3, 4, 1)
    
    def test_nonzero(self):
        assert self.get_target(1, 2, 0)
        assert not self.get_target()
    
    def test_len(self):
        assert len(self.get_target()) == 3

    def test_add(self):
        result = self.get_target(1, 2, 1) + self.get_target(5, 3, 1)
        assert result.x == 6
        assert result.y == 5
        assert result.z == 2

        result = self.get_target(1, 2, 3) + [5, 3, 4]
        assert result.x == 6
        assert result.y == 5
        assert result.z == 7
    
    def test_add_integer(self):
        result = self.get_target(2, 3, 1) + 6
        assert result.x == 8
        assert result.y == 9
        assert result.z == 7

    def test_radd_integer(self):
        result = 6 + self.get_target(2, 3, 1)
        assert result.x == 8
        assert result.y == 9
        assert result.z == 7

    def test_iadd(self):
        v = self.get_target(5, 2, 4)
        v += [2, 3, 2]
        assert v.x == 7
        assert v.y == 5
        assert v.z == 6
    
    def test_iadd_integer(self):
        v = self.get_target(5, 2, 2)
        v += 3
        assert v.x == 8
        assert v.y == 5
        assert v.z == 5
    
    def test_sub(self):
        result = self.get_target(4, 4, 1) - self.get_target(1, 2, 3)
        assert result.x == 3
        assert result.y == 2
        assert result.z == -2

        result = self.get_target(4, 4, 0) - (1, 2, 5)
        assert result.x == 3
        assert result.y == 2
        assert result.z == -5

    def test_sub_integer(self):
        result = self.get_target(4, 4, 10) - 3
        assert result.x == 1
        assert result.y == 1
        assert result.z == 7

    def test_rsub(self):
        result = [10, 5, 4] - self.get_target(4, 3, 3)
        assert result.x == 6
        assert result.y == 2
        assert result.z == 1

    def test_rsub_integer(self):
        result = 10 - self.get_target(4, 3, 9)
        assert result.x == 6
        assert result.y == 7
        assert result.z == 1

    def test_isub(self):
        v = self.get_target(5, 6, 4)
        v -= self.get_target(2, 1, 2)
        assert v.x == 3
        assert v.y == 5
        assert v.z == 2

        v = (2, 3, 5)
        v -= self.get_target(1, 1, 1)
        assert v.x == 1
        assert v.y == 2
        assert v.z == 4

    def test_isub_integer(self):
        v = self.get_target(3, 4)
        v -= 2
        assert v.x == 1
        assert v.y == 2

        v = 10
        v -= self.get_target(3, 4)
        assert v.x == 7
        assert v.y == 6

    def test_mul(self):
        result = self.get_target(2, 3, 1) * self.get_target(2, 2, 2)
        assert result.x == 4
        assert result.y == 6
        assert result.z == 2

        result = self.get_target(5, 3, 3) * [2, 2, 3]
        assert result.x == 10
        assert result.y == 6
        assert result.z == 9

    def test_mul_integer(self):
        result = self.get_target(3, 5, 2) * 3
        assert result.x == 9
        assert result.y == 15
        assert result.z == 6

    def test_rmul_integer(self):
        result = 5*self.get_target(2, 3, 1)
        assert result.x == 10
        assert result.y == 15
        assert result.z == 5

    def test_imul(self):
        v = self.get_target(5, 2, 6)
        v *= [2, 3, 2]
        assert v.x == 10
        assert v.y == 6
        assert v.z == 12
    
    def test_imul_integer(self):
        v = self.get_target(5, 2, 4)
        v *= 3
        assert v.x == 15
        assert v.y == 6
        assert v.z == 12
    
    def test_neg(self):
        v = -self.get_target(4, -2, 1)
        assert v.x == -4
        assert v.y == 2
        assert v.z == -1

    def test_ge(self):
        v = self.get_target(1, 1, 1)
        assert v >= (0, 0, 0)
        assert v >= (1, 1, 1)
        assert v >= 0
        assert v >= 1
        assert not v >= (4, 0, 0)

    def test_gt(self):
        v = self.get_target(1, 1, 1)
        assert v > (0, 0, 0)
        assert not v > (1, 1, 1)
        assert v > 0
        assert not v > 1

    def test_le(self):
        v = self.get_target(1, 1, 1)
        assert v <= (4, 4, 4)
        assert v <= (1, 1, 1)
        assert v <= 2
        assert v <= 1
        assert not v <= (4, 0, 0)

    def test_gt(self):
        v = self.get_target(1, 1, 1)
        assert v < (3, 2, 2)
        assert not v < (1, 1, 1)
        assert v < 2
        assert not v < 1

    def test_abs(self):
        v = self.get_target(2, 3, 2)
        result = abs(v)
        self.assertAlmostEquals(result, 4.1231056)

        assert v.__abs__ == v.magnitude


if __name__ == '__main__':
    unittest.main()